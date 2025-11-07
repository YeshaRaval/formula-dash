# F1 Data Update Guide

## How to Update F1 Data from Kaggle

### Step 1: Download New Data
1. Go to https://www.kaggle.com/datasets/jtrotman/formula-1-race-data
2. Click "Download" to get the latest dataset
3. Extract the ZIP file

### Step 2: Prepare for Merge
1. Create a folder called `f1_data_new` in your project directory
2. Copy all CSV files from the downloaded Kaggle data into `f1_data_new/`

### Step 3: Run the Merge Script
```bash
python merge_f1_data.py
```

### What the Script Does
- ✓ Creates automatic backup of your existing data
- ✓ Merges new records with existing data
- ✓ Updates existing records if they changed
- ✓ Never deletes existing data
- ✓ Handles all 15+ CSV files automatically

### After Merging
1. Test your application locally to ensure everything works
2. Commit and push the updated data:
```bash
git add f1_data/
git commit -m "Update F1 data from Kaggle"
git push
```

### Rollback (if needed)
If something goes wrong, your backup is saved in a folder like:
`f1_data_backup_20251107_183045/`

To restore:
```bash
rm -rf f1_data/
mv f1_data_backup_YYYYMMDD_HHMMSS/ f1_data/
```

## File Structure
```
project/
├── f1_data/              # Your current data (will be updated)
├── f1_data_new/          # Place new Kaggle data here
├── merge_f1_data.py      # The merge script
└── f1_data_backup_*/     # Automatic backups (created by script)
```
