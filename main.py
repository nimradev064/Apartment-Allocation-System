from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import pandas as pd
import random
import os
import shutil

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Constants
RESOURCE_FOLDER = 'Resources'
ORIGINAL_FOLDER = 'Original_Folder'
FINAL_OUTPUT_FILE = 'Final_output.xlsx'
FILES = [f'{RESOURCE_FOLDER}/Block_A.xlsx', f'{RESOURCE_FOLDER}/Block_B.xlsx', f'{RESOURCE_FOLDER}/Block_C.xlsx']
BLOCK_NAMES = {
    f'{RESOURCE_FOLDER}/Block_A.xlsx': 'A',
    f'{RESOURCE_FOLDER}/Block_B.xlsx': 'B',
    f'{RESOURCE_FOLDER}/Block_C.xlsx': 'C'
}
TOTAL_ROWS_PER_BLOCK = {
    'A': 140,
    'B': 140,
    'C': 17
}
EXPECTED_COLUMNS = ['Customer Name', 'Number of Rooms', 'Type of Apartment']


@app.get("/records")
def get_random_record():
    try:
        # Load DataFrames
        dfs = [pd.read_excel(f) for f in FILES]

        # Validate columns
        for i, df in enumerate(dfs):
            if not all(col in df.columns for col in EXPECTED_COLUMNS):
                raise HTTPException(status_code=400, detail=f"{FILES[i]} is missing required columns")

        # Check if all are empty
        if all(df.empty for df in dfs):
            raise HTTPException(status_code=404, detail="All Excel files are empty. No more records available.")

        # Choose a non-empty DataFrame
        non_empty_indices = [i for i, df in enumerate(dfs) if not df.empty]
        file_idx = random.choice(non_empty_indices)
        df = dfs[file_idx]

        # Randomly select and remove a row
        idx = random.choice(df.index)
        selected_row = df.loc[idx]
        dfs[file_idx] = df.drop(idx)

        block_file = FILES[file_idx]
        block_name = BLOCK_NAMES[block_file]

        # Append to Final_output
        if os.path.exists(FINAL_OUTPUT_FILE):
            final_output = pd.read_excel(FINAL_OUTPUT_FILE)
        else:
            final_output = pd.DataFrame(columns=EXPECTED_COLUMNS + ['Block'])

        selected_row_with_block = selected_row.copy()
        selected_row_with_block['Block'] = block_name
        final_output = pd.concat([final_output, selected_row_with_block.to_frame().T], ignore_index=True)

        # Save updated files
        for i, df in enumerate(dfs):
            df.to_excel(FILES[i], index=False)
        final_output.to_excel(FINAL_OUTPUT_FILE, index=False)

        # Prepare response
        Customer_Name = str(selected_row['Customer Name'])
        Number_of_Rooms = int(selected_row['Number of Rooms'])
        Type_of_Apartment = str(selected_row['Type of Apartment'])
        Part_A, _ = Type_of_Apartment.split(" ", 1)
        Flat_ID = block_name + " " + str(selected_row.get('FlatID', "N/A"))
        Remaining = sum(len(df) for df in dfs)
        Total = sum(TOTAL_ROWS_PER_BLOCK.values())

        return {
            "Block": block_name,
            "Customer_Name": Customer_Name,
            "Number_of_Rooms": Number_of_Rooms,
            "Type_of_Apartment": Part_A,
            "Flat_ID": Flat_ID,
            "Remaining_Records": Remaining,
            "Total_Rows_in_Block": Total
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
