# Repair Discount Module for Odoo 13

This module adds a discount field to the Repair Orders quotation lines in both the Parts and Operations tabs. The discount is applied per line, calculated before tax, and updates the line total dynamically.

## Features

- Adds a discount field to the repair line items.
- Calculates the subtotal after applying the discount before tax.
- Updates the line total dynamically based on the discount applied.

## Installation

1. Place the `repair_discount` directory in your Odoo addons path.
2. Update the app list in Odoo.
3. Install the `repair_discount` module from the Apps menu.

## Usage

- Navigate to the Repair Orders.
- In the Parts and Operations tabs, you will see a new field for discount on each line.
- Enter the discount amount, and the subtotal will update automatically before tax.

## Compatibility

This module is compatible with Odoo 13 and may require adjustments for other versions.

## Author

RandC Infosolutions

## License

This module is licensed under the terms of the GNU General Public License v3.0.