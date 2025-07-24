import pandas as pd
import os
from itemInfo import category_data

def save_all_to_excel(output_dir="output", base_filename="sysco_full_product_data") -> None:
    os.makedirs(output_dir, exist_ok=True)

    excel_path = os.path.join(output_dir, f"{base_filename}.xlsx")
    csv_path = os.path.join(output_dir, f"{base_filename}.csv")

    all_rows = []

    # keep the order fot the first cols
    base_fields = [
        "Brand Name", "Product Name", "Packaging Information",
        "SKU", "Picture URL", "Description"
    ]

    with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
        for category, items in category_data.items():
            # find all the keys in the category
            all_keys = set()
            for item in items:
                all_keys.update(item.keys())

            # all the other cols 
            dynamic_keys = sorted(k for k in all_keys if k not in base_fields)

            # order by cols
            final_columns = base_fields + dynamic_keys

            # list of all cols
            normalized_items = []
            for item in items:
                row = {key: item.get(key, "") for key in final_columns}
                normalized_items.append(row)

            df = pd.DataFrame(normalized_items)
            sheet_name = category[:31]  # limit the sheet nems for 32 letter
            df.to_excel(writer, sheet_name=sheet_name, index=False)

            for row in normalized_items:
                row["Category"] = category
                all_rows.append(row)

    # write all to one csv
    if all_rows:
        # use every category in the same sheet
        all_keys_csv = set()
        for row in all_rows:
            all_keys_csv.update(row.keys())

        dynamic_keys_csv = sorted(k for k in all_keys_csv if k not in base_fields + ["Category"])
        final_columns_csv = base_fields + dynamic_keys_csv + ["Category"]

        df_all = pd.DataFrame(all_rows)
        df_all = df_all.reindex(columns=final_columns_csv)  # order
        df_all.to_csv(csv_path, index=False)

    print(f"Excel file saved to: {os.path.abspath(excel_path)}")
    print(f"CSV file saved to: {os.path.abspath(csv_path)}")
