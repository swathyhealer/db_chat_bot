from schema import Invoice, InvoiceItem
from db_session import session
import ast
from datetime import datetime, timedelta


def insert_invoice(invoice_data: str):
    """
    Inserts a new invoice into the database.

    Args:

        invoice_data :
        {
            "id": "<invoice id>",
            "customer_name": "customer name",
            "date": "<date in YYYY-MM-DD>",
            "total_amount": <total amount in invoice>,
            "items": [<lineitem 1>, <lineitem 2>]
        }

    Returns:
        Invoice: The created invoice object.
    """

    invoice_data = ast.literal_eval(invoice_data)
    if "date" in invoice_data:
        date_obj = datetime.strptime("2025-03-07", "%Y-%m-%d").date()
        invoice_data["date"] = date_obj
    invoice = Invoice(
        id=int(invoice_data["id"]),
        customer_name=invoice_data["customer_name"],
        date=invoice_data["date"],
        total_amount=invoice_data["total_amount"],
    )

    for item in invoice_data["items"]:
        invoice.items.append(
            InvoiceItem(
                description=item["description"],
                quantity=item["quantity"],
                unit_price=item["unit_price"],
            )
        )

    session.add(invoice)
    session.commit()
    session.refresh(invoice)
    print("all value")
    invoices = session.query(Invoice).all()  # Fetch all invoices
    for invoice in invoices:
        print(invoice)
        print(invoice.id, invoice.customer_name, invoice.total_amount)
    return str(invoice)


def update_invoice(invoice_id: int, updated_data: str):
    """
    Updates an existing invoice in the database.

    Args:

        invoice_id (int): ID of the invoice to update.
        updated_data (dict): Dictionary containing updated fields.

    Returns:
        Invoice: The updated invoice object.
    """
    print(invoice_id)
    print(type(invoice_id))
    print(updated_data)
    updated_data = ast.literal_eval(updated_data)
    invoice = session.query(Invoice).filter_by(id=int(invoice_id)).first()
    print("retrieved invoice:", invoice)
    if not invoice:
        return None  # Invoice not found
    if "date" in updated_data:
        date_obj = datetime.strptime(updated_data["date"], "%Y-%m-%d").date()
        updated_data["date"] = date_obj
    if "customer_name" in updated_data:
        invoice.customer_name = updated_data.get("customer_name")
    if "date" in updated_data:
        invoice.date = updated_data.get("date")
    if "total_amount" in updated_data:
        invoice.total_amount = updated_data.get("total_amount")
    # invoice.total_amount = updated_data.get('total_amount', invoice.total_amount)
    # invoice.items=invoice.items
    # if 'items' in updated_data:
    #     invoice.items.clear()  # Remove old items
    #     for item in updated_data['items']:
    #         invoice.items.append(InvoiceItem(
    #             description=item['description'],
    #             quantity=item['quantity'],
    #             unit_price=item['unit_price']
    #         ))
    invoice.updated_at = datetime.utcnow()
    session.commit()
    session.refresh(invoice)

    return str(invoice)


def show_invoice(invoice_id: int):
    """
    Retrieves an invoice from the database.

    Args:

        invoice_id (int): ID of the invoice to retrieve.

    Returns:
        dict: Dictionary representation of the invoice, including items.
    """
    print(invoice_id)
    print(type(invoice_id))
    invoice = session.query(Invoice).filter_by(id=invoice_id).first()
    print("retrived invoice", invoice)
    if not invoice:
        return None  # Invoice not found

    return str(invoice.__dict__)


def get_last_week_invoices():
    """
    Retrieves invoices that were updated within the last week.

    Args:
        session (Session): SQLAlchemy session object.

    Returns:
        list: A list of invoice dictionaries updated in the last week.
    """
    one_week_ago = datetime.utcnow() - timedelta(days=7)
    invoices = session.query(Invoice).filter(Invoice.updated_at >= one_week_ago).all()

    return str([invoice.__dict__ for invoice in invoices])
