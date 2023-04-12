import xml.etree.ElementTree as ET
import json
import parsers.config_parser

# Remove duplicate items from the items_node based on their description
def remove_duplicates(items_node):
    unique_descriptions = set()
    for item_node in list(items_node):
        description = item_node.find("Description").text
        if description in unique_descriptions:
            items_node.remove(item_node)
        else:
            unique_descriptions.add(description)
    return items_node

# Update the SKU and price of the item_node based on the description
def update_sku_price(item_node, sku_dict, price_dict):
    description = item_node.find("Description").text
    if description in sku_dict:
        item_node.find("SKU").text = sku_dict[description]
        item_node.find("Price").text = price_dict[description]
    else:
        sku = item_node.find("SKU").text
        price = item_node.find("Price").text
        sku_dict[description] = sku
        price_dict[description] = price
    return item_node, sku_dict, price_dict

# Apply inflation based on the order_date to the price and quantity
def apply_inflation(order_date, price, quantity):
    if order_date >= '2021-01-01' and order_date < '2022-01-01':
        price *= 1.05
    elif order_date >= '2022-01-01' and order_date < '2023-01-01':
        price *= 1.10
    elif order_date >= '2023-01-01':
        price *= 1.20
        quantity += 3
    return price, quantity

# Calculate the total price of all items in the items_node
def calculate_total_price(items_node):
    total_price = 0
    for item_node in items_node:
        quantity = int(item_node.find("Quantity").text)
        price = float(item_node.find("Price").text)
        total_price += quantity * price
    return total_price

# Update the items with inflated prices and quantities based on the order_date
def update_items_with_inflation(items, order_date):
    for item_node in items:
        price = float(item_node.find("Price").text)
        quantity = int(item_node.find("Quantity").text)
        price, quantity = apply_inflation(order_date, price, quantity)
        item_node.find("Price").text = str(price)
        item_node.find("Quantity").text = str(quantity)
    return items

# Generate general instructions based on the dataset
def generate_general_instructions(dataset):
    # Extract relevant information from the dataset
    order_id = dataset['order_id']
    order_date = dataset['order_date']
    seller = dataset['seller']
    customer_email = dataset['customer_email']
    customer_id = dataset['customer_id']
    total_price = round(dataset['total_price'], 2)
    total_quantity = dataset['total_quantity']

    # Create instructions as a list of dictionaries
    instructions = [
        # Add instructions for the total cost of the order, seller, date, customer email, and total quantity
        {
        "instruction": f"Question : What was the total cost of the order with ID '{order_id}'?",
        "input": "",
        "output": f"Answer : The total cost of the order was ${total_price}"
    },
    {
        "instruction": f"Question : Who was the seller for the order with ID '{order_id}'?",
        "input": "",
        "output": f"Answer : The seller for the order with ID '{order_id}' was {seller}."
    },
    {
        "instruction": f"Question : What was the date of the sales order with ID '{order_id}'?",
        "input": "",
        "output": f"Answer : The date of the sales order with ID '{order_id}' was '{order_date}'."
    },
    {
        "instruction": f"Question : What is the email address of the customer with ID '{order_id}'?",
        "input": "",
        "output": f"Answer : The email address of the customer with ID '{customer_id}' was '{customer_email}'."
    },
    {
        "instruction": f"Question : What is the total quantity of items ordered in the sales order with ID '{order_id}'?",
        "input": "",
        "output": f"Answer : The total quantity of items ordered in the sales order with ID '{order_id}' was {total_quantity}."
    },
    ]
    return instructions

# Generate item-specific instructions based on the item_node
def generate_item_instructions(item_node):
    # Extract relevant information from the item_node
    sku = item_node.find('SKU').text
    description = item_node.find('Description').text
    quantity = int(item_node.find('Quantity').text)
    price = float(item_node.find('Price').text)
    item_cost = round(quantity * price, 2)

    instructions = [
            {'instruction': f"What is the cost of item '{sku}'?",
            'input': '', 'output': f"The cost of item '{sku}' was ${item_cost}."},
            {'instruction': f"What is the name of item '{sku}'?",
            'input': '', 'output': f"The name of item '{sku}' was '{description}'."},
            {'instruction': f"What is the SKU of item '{description}'?",
            'input': '', 'output': f"The SKU of item '{description}' was '{sku}'."}
        ]
    # Create instructions as a list of dictionaries
    """instructions = [
        {'instruction': f"Question : What is the cost of item '{sku}'?",
         'input': '', 'output': f"Answer : The cost of item '{sku}' was ${item_cost}."},
        {'instruction': f"Question : What is the name of item '{sku}'?",
         'input': '', 'output': f"Answer : The name of item '{sku}' was '{description}'."},
        {'instruction': f"Question : What is the SKU of item '{description}'?",
         'input': '', 'output': f"Answer : The SKU of item '{description}' was '{sku}'."}
    ]"""

    return instructions


def dataset_pretreatment_custom(dataset):
    order_date = dataset['order_date']
    order_id = dataset['order_id']
    items = dataset['items']
    sku_dict = {}
    price_dict = {}

    # Remove duplicates and update SKU and price
    items = remove_duplicates(items)
    for item_node in items:
        item_node, sku_dict, price_dict = update_sku_price(item_node, sku_dict, price_dict)

    # Apply inflation and update quantity
    items = update_items_with_inflation(items, order_date)

    # Calculate and add total price to XML
    total_price = calculate_total_price(items)
    total_quantity = sum([int(i.find('Quantity').text) for i in items])

    seller = dataset['seller']
    customer_email = dataset['customer_email']
    customer_id = dataset['customer_id']

    treated_dataset = {
        'order_id': order_id,
        'order_date': order_date,
        'items': items,
        'total_price': total_price,
        'total_quantity': total_quantity,
        'seller': seller,
        'customer_email': customer_email,
        'customer_id': customer_id
    }
    return treated_dataset


def generate_instructions_custom(dataset):
    items = dataset['items']
    entries = []

    for i, item_node in enumerate(items):
        # Generate the question-answer pairs for each item
        instructions = []
        if i == 0:
            instructions.extend(generate_general_instructions(dataset))

        instructions.extend(generate_item_instructions(item_node))

        entries.extend(instructions)

    return entries



