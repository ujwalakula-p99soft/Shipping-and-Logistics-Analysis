from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_FILE  = PROJECT_ROOT / "data" / "raw" / "superstore.csv"
OUTPUT_DIR   = PROJECT_ROOT / "data" / "raw"
NUM_BATCHES  = 4


def main():
    print(f"Reading: {SOURCE_FILE}")

    df = pd.read_csv(SOURCE_FILE)

    df.columns = (
        df.columns.str.lower()
        .str.replace(" ", "_", regex=False)
        .str.replace("-", "_", regex=False)
        .str.replace(".", "_", regex=False)
    )

    df["order_date"] = pd.to_datetime(df["order_date"])
    df["ship_date"]  = pd.to_datetime(df["ship_date"])
    df = df.sort_values("order_date").reset_index(drop=True)

    batch_size = len(df) // NUM_BATCHES

    for i in range(NUM_BATCHES):
        start = i * batch_size
        end   = (i + 1) * batch_size if i < NUM_BATCHES - 1 else len(df)

        batch = df.iloc[start:end].copy()
        batch["order_date"] = batch["order_date"].dt.strftime("%Y-%m-%d 00:00:00.000")
        batch["ship_date"]  = batch["ship_date"].dt.strftime("%Y-%m-%d 00:00:00.000")

        out = OUTPUT_DIR / f"batch_{i + 1:02d}.csv"
        batch.to_csv(out, index=False)
        print(f"Created {out.name} ({len(batch)} rows)")

    print("Done.")


if __name__ == "__main__":
    main()
