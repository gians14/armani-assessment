import pandas as pd


class EanStats:
    def __init__(self, df_transactions_read, df_prices_read):

        self.df_transactions_read = df_transactions_read
        self.df_prices_read = df_prices_read

    def transaction_preparation(self):

        country_adaption = {
            "AUD": "Australia",
            "BRL": "Brasil",
            "CAD": "Canada",
            "CNY": "China",
            "EUR": "Undefined_EUR",
            "JPY": "Japan",
            "MXN": "Mexico",
            "USD": "Undefined_USD",
        }

        df_transactions = self.df_transactions_read.copy()
        df_transactions["COUNTRY"] = df_transactions["COUNTRY"].fillna(
            df_transactions["CURRENCY"].map(country_adaption)
        )
        df_transactions = df_transactions[df_transactions["EAN"].notna()]
        df_transactions = df_transactions[df_transactions["QUANTITY"].notna()]
        df_transactions["AMOUNT"] = df_transactions["AMOUNT"].astype("double")
        df_transactions = df_transactions[df_transactions["AMOUNT"] > 0]
        df_transactions["QUANTITY"] = df_transactions["QUANTITY"].astype("int64")
        df_transactions["DATE"] = df_transactions["DATE"].str[:10]
        df_transactions.loc[
            df_transactions.COUNTRY == "USA", "COUNTRY"
        ] = "United States"
        df_transactions.loc[
            df_transactions.COUNTRY.isin(["Japan", "South Korea"]), "AMOUNT"
        ] = (df_transactions.AMOUNT / 100)

        return df_transactions

    def prices_preparation(self):

        df_prices = self.df_prices_read.copy()
        to_double_column = list(df_prices.columns.values)
        to_double_column.remove("EAN")

        df_prices[[*to_double_column]] = df_prices[[*to_double_column]].astype("float")
        df_prices_unpivotted = df_prices.melt(
            id_vars=["EAN"], var_name="COUNTRY", value_name="LIST_PRICE"
        )
        df_prices_unpivotted.loc[
            df_prices_unpivotted.COUNTRY == "Mexico", "LIST_PRICE"
        ] = (df_prices_unpivotted.LIST_PRICE * 25)

        return df_prices_unpivotted

    @staticmethod
    def pre_stats(df_transactions, df_prices_unpivotted):

        df_for_stats = df_transactions[
            ["EAN", "AMOUNT", "QUANTITY", "COUNTRY", "TRANSACTION ID"]
        ].merge(df_prices_unpivotted, on=["EAN", "COUNTRY"], how="left")

        print(df_for_stats.head())
        df_for_stats["RATIO_PRICE"] = round(
            df_for_stats["AMOUNT"] / df_for_stats["LIST_PRICE"], 2
        )
        df_for_stats["DELTA_PRICE"] = (
            df_for_stats["AMOUNT"] - df_for_stats["LIST_PRICE"]
        )
        df_for_stats["TOTAL_AMOUNT"] = df_for_stats["AMOUNT"] * df_for_stats["QUANTITY"]

        return df_for_stats

    @staticmethod
    def stats(df_for_stats):

        stats = {}
        stats_typology = ["SOLD", "RETURN"]
        stats_measure = ["QUANTITY", "TOTAL_AMOUNT"]

        for typology in stats_typology:
            if typology == "SOLD":
                df_for_stats_filtered = df_for_stats[df_for_stats.QUANTITY > 0]
            else:
                df_for_stats_filtered = df_for_stats[df_for_stats.QUANTITY < 0]
            for stat in stats_measure:
                stats[typology + "_" + stat] = (
                    pd.DataFrame(
                        {
                            stat: df_for_stats_filtered.groupby(
                                ["EAN", "COUNTRY"], as_index=False
                            )[stat]
                            .sum()
                            .groupby("EAN")
                            .apply(lambda x: dict(zip(x["COUNTRY"], x[stat])))
                        }
                    )
                    .reset_index()
                    .rename(columns={stat: typology + "_" + stat})
                )

        stat = "RATIO_PRICE" 
        stats[stat] = pd.DataFrame({stat: round(df_for_stats[["EAN", "RATIO_PRICE"]].dropna()\
                                            .groupby(["EAN"])["RATIO_PRICE"].mean(),2)})\
                                            .reset_index()
    
        stat = "COUNTRY_RATIO_PRICE" 
        stats[stat] = pd.DataFrame({stat: round(df_for_stats[["EAN", "COUNTRY", "RATIO_PRICE"]].dropna()\
                                            .groupby(["EAN", "COUNTRY"], as_index=False)["RATIO_PRICE"].mean(),2)\
                                            .groupby("EAN").apply(lambda x: dict(zip(x["COUNTRY"], x["RATIO_PRICE"])))})\
                                            .reset_index()

        return (
            stats["SOLD_QUANTITY"]
            .merge(stats["SOLD_TOTAL_AMOUNT"], on="EAN", how="outer")
            .merge(stats["RETURN_QUANTITY"], on="EAN", how="outer")
            .merge(stats["RETURN_TOTAL_AMOUNT"], on="EAN", how="outer")
            .merge(stats["RATIO_PRICE"], on="EAN", how="outer")
            .merge(stats["COUNTRY_RATIO_PRICE"], on="EAN", how="outer")
        )
