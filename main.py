# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import FileResponse
# import pandas as pd
# import random
# import os
# import shutil

# app = FastAPI()

# # Configure CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Allows all origins
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # # Constants
# # RESOURCE_FOLDER = 'Resources'
# # ORIGINAL_FOLDER = 'Original_Folder'
# # FINAL_OUTPUT_FILE = 'Final_output.xlsx'
# # FILES = [f'{RESOURCE_FOLDER}/Block_A.xlsx', f'{RESOURCE_FOLDER}/Block_B.xlsx', f'{RESOURCE_FOLDER}/Block_C.xlsx']
# # BLOCK_NAMES = {
# #     f'{RESOURCE_FOLDER}/Block_A.xlsx': 'A',
# #     f'{RESOURCE_FOLDER}/Block_B.xlsx': 'B',
# #     f'{RESOURCE_FOLDER}/Block_C.xlsx': 'C'
# # }
# # TOTAL_ROWS_PER_BLOCK = {
# #     'A': 140,
# #     'B': 140,
# #     'C': 17
# # }
# # EXPECTED_COLUMNS = ['Customer Name', 'Number of Rooms', 'Type of Apartment']


# # @app.get("/records")
# # def get_random_record():
# #     try:
# #         # Load DataFrames
# #         dfs = [pd.read_excel(f) for f in FILES]

# #         # Validate columns
# #         for i, df in enumerate(dfs):
# #             if not all(col in df.columns for col in EXPECTED_COLUMNS):
# #                 raise HTTPException(status_code=400, detail=f"{FILES[i]} is missing required columns")

# #         # Check if all are empty
# #         if all(df.empty for df in dfs):
# #             raise HTTPException(status_code=404, detail="All Excel files are empty. No more records available.")

# #         # Choose a non-empty DataFrame
# #         non_empty_indices = [i for i, df in enumerate(dfs) if not df.empty]
# #         file_idx = random.choice(non_empty_indices)
# #         df = dfs[file_idx]

# #         # Randomly select and remove a row
# #         idx = random.choice(df.index)
# #         selected_row = df.loc[idx]
# #         dfs[file_idx] = df.drop(idx)

# #         block_file = FILES[file_idx]
# #         block_name = BLOCK_NAMES[block_file]

# #         # Append to Final_output
# #         if os.path.exists(FINAL_OUTPUT_FILE):
# #             final_output = pd.read_excel(FINAL_OUTPUT_FILE)
# #         else:
# #             final_output = pd.DataFrame(columns=EXPECTED_COLUMNS + ['Block'])

# #         selected_row_with_block = selected_row.copy()
# #         selected_row_with_block['Block'] = block_name
# #         final_output = pd.concat([final_output, selected_row_with_block.to_frame().T], ignore_index=True)

# #         # Save updated files
# #         for i, df in enumerate(dfs):
# #             df.to_excel(FILES[i], index=False)
# #         final_output.to_excel(FINAL_OUTPUT_FILE, index=False)

# #         # Prepare response
# #         Customer_Name = str(selected_row['Customer Name'])
# #         Number_of_Rooms = int(selected_row['Number of Rooms'])
# #         Type_of_Apartment = str(selected_row['Type of Apartment'])
# #         Part_A, _ = Type_of_Apartment.split(" ", 1)
# #         Flat_ID = block_name + " " + str(selected_row.get('FlatID', "N/A"))
# #         Remaining = sum(len(df) for df in dfs)
# #         Total = sum(TOTAL_ROWS_PER_BLOCK.values())

# #         return {
# #             "Block": block_name,
# #             "Customer_Name": Customer_Name,
# #             "Number_of_Rooms": Number_of_Rooms,
# #             "Type_of_Apartment": Part_A,
# #             "Flat_ID": Flat_ID,
# #             "Remaining_Records": Remaining,
# #             "Total_Rows_in_Block": Total
# #         }

# #     except Exception as e:
# #         raise HTTPException(status_code=500, detail=str(e))


# # @app.get("/download")
# # def download_final_output():
# #     if not os.path.exists(FINAL_OUTPUT_FILE):
# #         raise HTTPException(status_code=404, detail="Final output file not found.")
# #     return FileResponse(path=FINAL_OUTPUT_FILE, filename="Final_output.xlsx", media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


# # @app.get("/reset")
# # def reset_data_files():
# #     try:
# #         # Delete Final_output.xlsx
# #         if os.path.exists(FINAL_OUTPUT_FILE):
# #             os.remove(FINAL_OUTPUT_FILE)

# #         # Delete all Excel files in Resources folder
# #         for file in os.listdir(RESOURCE_FOLDER):
# #             if file.endswith('.xlsx'):
# #                 os.remove(os.path.join(RESOURCE_FOLDER, file))

# #         # Copy files from Original_Folder to Resources
# #         for file in os.listdir(ORIGINAL_FOLDER):
# #             if file.endswith('.xlsx'):
# #                 shutil.copyfile(
# #                     os.path.join(ORIGINAL_FOLDER, file),
# #                     os.path.join(RESOURCE_FOLDER, file)
# #                 )

# #         return {"message": "Reset successful. All files restored from Original_Folder."}

# #     except Exception as e:
# #         raise HTTPException(status_code=500, detail=f"Reset failed: {str(e)}")




from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import pandas as pd
import random
import os
import shutil

app = FastAPI()

# Constants
RESOURCE_FOLDER = 'results'
FINAL_OUTPUT_FILE = 'Final_output.xlsx'
FILES = [
    f'{RESOURCE_FOLDER}/Block_R.xlsx',
    f'{RESOURCE_FOLDER}/Block_C0.xlsx',
    f'{RESOURCE_FOLDER}/Block_C1.xlsx'
]
TOTAL_ROWS_PER_BLOCK = {
    'R': 297,
    'C0': 15,
    'C1': 41
}

ORIGINAL_FOLDER = 'Original_Results'
EXPECTED_COLUMNS = ['Customer Name', 'Number of Rooms', 'Type of Apartment', 'Block']

@app.get("/records")
def get_record():
    try:
        # Load all DataFrames
        dfs = {file: pd.read_excel(file) for file in FILES}

        # Validate required columns
        for file, df in dfs.items():
            if not all(col in df.columns for col in EXPECTED_COLUMNS):
                raise HTTPException(status_code=400, detail=f"{file} is missing required columns")

        # Check if all files are empty
        if all(df.empty for df in dfs.values()):
            raise HTTPException(status_code=404, detail="All Excel files are empty. No records available.")

        # Use Block_R first
        block_r_file = f'{RESOURCE_FOLDER}/Block_R.xlsx'
        if not dfs[block_r_file].empty:
            selected_file = block_r_file
        else:
            # Randomly choose from Block_C0 or Block_C1
            fallback_files = [f for f in FILES if f != block_r_file and not dfs[f].empty]
            if not fallback_files:
                raise HTTPException(status_code=404, detail="No records left in any block.")
            selected_file = random.choice(fallback_files)

        # Select a random row from the chosen block
        df = dfs[selected_file]
        idx = random.choice(df.index)
        selected_row = df.loc[idx]
        dfs[selected_file] = df.drop(idx)

        # Append to Final_output
        if os.path.exists(FINAL_OUTPUT_FILE):
            final_output = pd.read_excel(FINAL_OUTPUT_FILE)
        else:
            final_output = pd.DataFrame(columns=EXPECTED_COLUMNS)

        final_output = pd.concat([final_output, selected_row.to_frame().T], ignore_index=True)

        # Save updated Excel files
        for file, df in dfs.items():
            df.to_excel(file, index=False)
        final_output.to_excel(FINAL_OUTPUT_FILE, index=False)

        # Prepare response
        block = str(selected_row['Block'])
        customer_name = str(selected_row['Customer Name'])
        number_of_rooms = int(selected_row['Number of Rooms'])
        type_of_apartment = str(selected_row['Type of Apartment'])
        part_a, _ = type_of_apartment.split(" ", 1) if " " in type_of_apartment else (type_of_apartment, "")
        flat_id = block + " " + str(selected_row.get('FlatID', "N/A"))
        remaining = sum(len(df) for df in dfs.values())
        total = sum(TOTAL_ROWS_PER_BLOCK.values())

        return {
            "Block": block,
            "Customer_Name": customer_name,
            "Number_of_Rooms": number_of_rooms,
            "Type_of_Apartment": part_a,
            "Flat_ID": flat_id,
            "Remaining_Records": remaining,
            "Total_Rows_in_Block": total
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.get("/download")
def download_final_output():
    if not os.path.exists(FINAL_OUTPUT_FILE):
        raise HTTPException(status_code=404, detail="Final output file not found.")
    return FileResponse(path=FINAL_OUTPUT_FILE, filename="Final_output.xlsx", media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')




@app.get("/reset")
def reset_data_files():
    try:
        # Delete Final_output.xlsx
        if os.path.exists(FINAL_OUTPUT_FILE):
            os.remove(FINAL_OUTPUT_FILE)

        # Delete all Excel files in Resources folder
        for file in os.listdir(RESOURCE_FOLDER):
            if file.endswith('.xlsx'):
                os.remove(os.path.join(RESOURCE_FOLDER, file))

        # Copy files from Original_Folder to Resources
        for file in os.listdir(ORIGINAL_FOLDER):
            if file.endswith('.xlsx'):
                shutil.copyfile(
                    os.path.join(ORIGINAL_FOLDER, file),
                    os.path.join(RESOURCE_FOLDER, file)
                )

        return {"message": "Reset successful. All files restored from Original_Folder."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Reset failed: {str(e)}")
