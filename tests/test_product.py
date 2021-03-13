import pytest
from flask import url_for

from app import db
from app.models import Product


def create_book(name="Sherlock Homes", description="a house hunting real estate agent"):
    book = Product(name="Sherlock Homes", description="a house hunting detective", price_cents=500)
    db.session.add(book)
    db.session.commit()
    return book


def test_product_creation(client, init_database):
    assert Product.query.count() == 0
    book = create_book()
    assert Product.query.count() == 1
    assert Product.query.first().name == book.name


def test_name_validation(client, init_database):
    with pytest.raises(ValueError):
        Product(name=" ", description="invalid book")


def test_index_page(client, init_database):
    book = create_book()
    response = client.get(url_for('products.index'))
    assert response.status_code == 200
    assert b'Yumroad' in response.data
    assert book.name in str(response.data)
    expected_link = url_for('products.details', product_id=book.id)
    assert expected_link in str(response.data)


def test_details_page(client, init_database):
    book = create_book()
    response = client.get(url_for('products.details', product_id=book.id))
    assert response.status_code == 200
    assert b'Yumroad' in response.data
    assert b'Buy for $5.00' in response.data
    assert book.name in str(response.data)


def test_non_existent_book(client, init_database, authenticated_request):
    book = create_book()
    response = client.get(url_for('products.details', product_id=book.id+1))
    assert response.status_code == 404


def test_new_page_unauthorized(client, init_database):
    response = client.get(url_for('products.create'))
    assert response.status_code == 302


def test_new_page(client, init_database, authenticated_request):
    response = client.get(url_for('products.create'))
    assert response.status_code == 200
    assert b'Name' in response.data
    assert b'Create' in response.data


def test_creation(client, init_database, authenticated_request):
    response = client.post(url_for('products.create'),
                           data=dict(name='test product', description='is persisted', price=5),
                           follow_redirects=True)
    assert response.status_code == 200
    assert b'test product' in response.data
    assert b'Buy for $5.00' in response.data


def test_creation_without_price(client, init_database, authenticated_request):
    response = client.post(url_for('products.create'),
                            data=dict(name='test product', description='is persisted'),
                            follow_redirects=True)

    assert response.status_code == 200
    assert b'test product' in response.data
    assert b'Sold out' in response.data


def test_invalid_creation(client, init_database, authenticated_request):
    response = client.post(url_for('products.create'),
                           data=dict(name='ab', description='is not valid'),
                           follow_redirects=True)
    assert response.status_code == 200
    assert b'is not valid' in response.data
    assert b'Field must be between' in response.data
    assert b'is-invalid' in response.data


def test_edit_page(client, init_database, authenticated_request):
    book = create_book()
    response = client.get(url_for('products.edit', product_id=book.id))
    assert response.status_code == 200
    assert book.description in str(response.data)
    assert book.name in str(response.data)
    assert b'Edit' in response.data


def test_edit_submission(client, init_database, authenticated_request):
    book = create_book()
    old_description = book.description
    old_name = book.name
    response = client.post(url_for('products.edit',
                           product_id=book.id),
                           data={'name': 'test-change', 'description': 'is persisted'},
                           follow_redirects=True)
    assert response.status_code == 200
    assert 'test-change' in str(response.data)
    assert 'is persisted' in str(response.data)
    assert old_description not in str(response.data)
    assert old_name not in str(response.data)
    assert b'Edit' not in response.data


def test_invalid_edit_submission(client, init_database, authenticated_request):
    book = create_book()
    old_description = book.description
    old_name = book.name
    response = client.post(url_for('products.edit', product_id=book.id),
                           data=dict(name='br0', description='is persisted'),
                           follow_redirects=True)
    assert response.status_code == 200
    assert b'br0' in response.data
    assert b'Field must be between 4 and 60 characters long' in response.data
    assert Product.query.get(book.id).description == old_description
    assert old_description not in str(response.data)
    assert old_name in str(response.data)  # It's still in the page title
    assert b'Edit' in response.data

