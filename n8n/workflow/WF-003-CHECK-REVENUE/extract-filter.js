const data =  
{
  
  
"row_number": 
14,
  
  
"col_1": 
1,
  
  
"CÔNG TY TNHH SAIGON ALH": 
"0318356230",
  
  
"col_4": 
"",
  
  
"col_5": 
"",
  
  
"col_6": 
"",
  
  
"col_7": 
18360000,
  
  
"col_8": 
24392000,
  
  
"col_10": 
6032000,
  
  
"col_11": 
"ĐÚNG",
  
  
"col_12": 
"",
  
  
"col_13": 
"10/03/2026",
  
  
"col_14": 
"",
  
  
"col_15": 
0,
  
  
"col_16": 
"",
  
  
"col_17": 
"Check nhóm 2CE và Rich - báo được",
  
  
"col_18": 
"",
  
  
"col_19": 
"",
  
  
"col_20": 
"Đã TT  đến Q2",
  
  
"col_21": 
"",
  
  
"col_22": 
"",
  
  
"col_23": 
"",
  
  
"Mã công ty": 
"2CE",
  
  
"Phải thu cuối kỳ": 
""
  
}

const allItems = $input.all();
let data;

if (allItems.length > 1) {
  data = allItems.map(item => item.json);
} else {
  const first = allItems[0].json;
  data = Array.isArray(first) ? first : Object.values(first);
}

// Skip rows 1-13, keep row 14 onward
const REAL_DATA_START_ROW = 14;
const cleanData = data.filter(row => Number(row.row_number) >= REAL_DATA_START_ROW);

// Rename columns - adjust these keys to match your actual data
const RENAME_MAP = {
  'col_1': 'STT',
  'col_2': 'Mã công ty',
  'CÔNG TY TNHH SAIGON ALH': 'Mã số thuế',
  'col_5': 'Phải thu ĐẦU KỲ',
  'col_6': 'Phải trả ĐẦU KỲ',
  'col_7': 'Phải thu TRONG KỲ',
  'col_8': 'Phải trả TRONG KỲ',
  'col_9': 'Phải thu CUỐI kỳ',
  'col_10': 'Phải trả CUỐI kỳ',
  'col_11': 'Ghi chú',
  'col_13': 'THỜI HẠN THANH TOÁN'
};

// Debug: show actual keys of the first row so we can see the real structure
if (cleanData.length > 0) {
  console.log('Available keys in first row:', Object.keys(cleanData[0]));
}

const renamedData = cleanData.map(row => {
  const newRow = { ...row };
  for (const [oldKey, newKey] of Object.entries(RENAME_MAP)) {
    if (oldKey in newRow) {
      newRow[newKey] = newRow[oldKey];
      if (oldKey !== newKey) delete newRow[oldKey];
    } else {
      console.log(`Warning: key "${oldKey}" not found in row`);
    }
  }
  return newRow;
});

return renamedData.map(row => ({ json: row }));