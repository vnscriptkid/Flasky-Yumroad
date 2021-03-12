import pytest
from flask import url_for

from app import db
from app.models import Product


@pytest.fixture
def sample_book(name="Sherlock Homes", description="a house hunting real estate agent"):
    book = Product(name=name, description=description)
    db.session.add(book)
    db.session.commit()
    return book


def test_product_creation(client, init_database):
    assert Product.query.count() == 0
    book = Product(name="Sherlock Homes", description="a house hunting detective")
    db.session.add(book)
    db.session.commit()
    assert Product.query.count() == 1
    assert Product.query.first().name == book.name


def test_name_validation(client, init_database):
    with pytest.raises(ValueError):
        Product(name=" ", description="invalid book")


def test_index_page(client, init_database, sample_book):
    response = client.get(url_for('products.index'))
    assert response.status_code == 200
    assert b'Yumroad' in response.data
    assert sample_book.name in str(response.data)
    expected_link = url_for('products.details', product_id=sample_book.id)
    assert expected_link in str(response.data)


def test_details_page(client, init_database, sample_book):
    response = client.get(url_for('products.details', product_id=sample_book.id))
    assert response.status_code == 200
    assert b'Yumroad' in response.data
    assert b'Purchase coming soon' in response.data
    assert sample_book.name in str(response.data)


def test_non_existent_book(client, init_database, sample_book):
    response = client.get(url_for('products.details', product_id=sample_book.id+1))
    assert response.status_code == 404

