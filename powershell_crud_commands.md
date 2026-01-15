**Installation:** pip install fastapi uvicorn



 					**API Base:** http://127.0.0.1:8000

 					**Interactive Documentation:** http://127.0.0.1:8000/docs

 					**Alternative Documentation:** http://127.0.0.1:8000/redoc



**Terminal 1 command:**

 			uvicorn main:app --reload



**Terminal2 commands:**

\# ==========================================

\# **FASTAPI CRUD OPERATIONS - POWERSHELL COMMANDS**

\# ==========================================



\# 1. CREATE - Add a new item

Invoke-RestMethod -Uri "http://127.0.0.1:8000/items/" -Method Post -ContentType "application/json" -Body '{"name": "Laptop", "description": "Gaming laptop", "price": 999.99}'



\# Create another item

Invoke-RestMethod -Uri "http://127.0.0.1:8000/items/" -Method Post -ContentType "application/json" -Body '{"name": "Phone", "description": "Smartphone", "price": 699.99}'



\# Create a third item

Invoke-RestMethod -Uri "http://127.0.0.1:8000/items/" -Method Post -ContentType "application/json" -Body '{"name": "Headphones", "description": "Wireless headphones", "price": 199.99}'



\# ==========================================



\# 2. READ - Get all items

Invoke-RestMethod -Uri "http://127.0.0.1:8000/items/" -Method Get



\# READ - Get specific item by ID

Invoke-RestMethod -Uri "http://127.0.0.1:8000/items/1" -Method Get



\# READ - Get another specific item

Invoke-RestMethod -Uri "http://127.0.0.1:8000/items/2" -Method Get



\# READ - Get third item

Invoke-RestMethod -Uri "http://127.0.0.1:8000/items/3" -Method Get



\# ==========================================



\# 3. UPDATE - Update an existing item (full update)

Invoke-RestMethod -Uri "http://127.0.0.1:8000/items/1" -Method Put -ContentType "application/json" -Body '{"name": "Updated Laptop", "description": "Updated gaming laptop with RTX", "price": 1299.99}'



\# UPDATE - Partial update (only name and price)

Invoke-RestMethod -Uri "http://127.0.0.1:8000/items/2" -Method Put -ContentType "application/json" -Body '{"name": "iPhone 15", "price": 799.99}'



\# UPDATE - Update only description

Invoke-RestMethod -Uri "http://127.0.0.1:8000/items/3" -Method Put -ContentType "application/json" -Body '{"description": "Premium noise-cancelling headphones"}'



\# ==========================================



\# 4. DELETE - Delete an item

Invoke-RestMethod -Uri "http://127.0.0.1:8000/items/1" -Method Delete



\# DELETE - Delete another item

Invoke-RestMethod -Uri "http://127.0.0.1:8000/items/2" -Method Delete



\# DELETE - Delete third item

Invoke-RestMethod -Uri "http://127.0.0.1:8000/items/3" -Method Delete



\# ==========================================



\# 5. ADDITIONAL USEFUL COMMANDS



\# Check if API is running (root endpoint)

Invoke-RestMethod -Uri "http://127.0.0.1:8000/" -Method Get



\# Try to get a non-existent item (will return 404 error)

Invoke-RestMethod -Uri "http://127.0.0.1:8000/items/999" -Method Get



\# Try to update a non-existent item (will return 404 error)

Invoke-RestMethod -Uri "http://127.0.0.1:8000/items/999" -Method Put -ContentType "application/json" -Body '{"name": "Test"}'



\# Try to delete a non-existent item (will return 404 error)

Invoke-RestMethod -Uri "http://127.0.0.1:8000/items/999" -Method Delete



\# ==========================================

\# TESTING SEQUENCE (Run these in order)

\# ==========================================



\# Step 1: Create some items

Write-Host "Creating items..." -ForegroundColor Green

Invoke-RestMethod -Uri "http://127.0.0.1:8000/items/" -Method Post -ContentType "application/json" -Body '{"name": "Laptop", "description": "Gaming laptop", "price": 999.99}'

Invoke-RestMethod -Uri "http://127.0.0.1:8000/items/" -Method Post -ContentType "application/json" -Body '{"name": "Phone", "description": "Smartphone", "price": 699.99}'



\# Step 2: Get all items

Write-Host "Getting all items..." -ForegroundColor Green

Invoke-RestMethod -Uri "http://127.0.0.1:8000/items/" -Method Get



\# Step 3: Get specific item

Write-Host "Getting item with ID 1..." -ForegroundColor Green

Invoke-RestMethod -Uri "http://127.0.0.1:8000/items/1" -Method Get



\# Step 4: Update an item

Write-Host "Updating item with ID 1..." -ForegroundColor Green

Invoke-RestMethod -Uri "http://127.0.0.1:8000/items/1" -Method Put -ContentType "application/json" -Body '{"name": "Updated Laptop", "price": 1199.99}'



\# Step 5: Get all items again to see the update

Write-Host "Getting all items after update..." -ForegroundColor Green

Invoke-RestMethod -Uri "http://127.0.0.1:8000/items/" -Method Get



\# Step 6: Delete an item

Write-Host "Deleting item with ID 1..." -ForegroundColor Green

Invoke-RestMethod -Uri "http://127.0.0.1:8000/items/1" -Method Delete



\# Step 7: Get all items to confirm deletion

Write-Host "Getting all items after deletion..." -ForegroundColor Green

Invoke-RestMethod -Uri "http://127.0.0.1:8000/items/" -Method Get

