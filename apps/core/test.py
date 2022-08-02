from django.test import TestCase, Client

from .models import Customer, Order

import decimal


class TestCustomer(TestCase):
    def setUp(self) -> None:
        self.customer = Customer.objects.create(name='ehsan', email='ehsan@gmail.com')

    def test_customer_retreive(self):
        """Test if customer retreived seccussfully"""
        self.assertTrue(self.customer)

    def test_customer_create(self):
        """Test if customer created seccussfully"""
        new_customer = Customer.objects.create(name='ali')
        self.assertEqual(new_customer.id, 2)

    def test_customer_update(self):
        """Test if customer updated seccussfully"""
        self.assertEqual(self.customer.name, 'ehsan')

        self.customer.name = 'reza'
        self.customer.save()
        self.assertNotEqual(self.customer.name, 'ehsan')
    
    def test_customer_delete(self):
        """Test if customer deleted seccussfully"""
        self.assertTrue(Customer.objects.filter(name=self.customer.name).exists())

        Customer.objects.filter(id=self.customer.id).delete()
        self.assertFalse(Customer.objects.filter(name=self.customer.name).exists())


class TestOrder(TestCase):
    def setUp(self) -> None:
        self.customer = Customer.objects.create(name='ehsan', email='ehsan@gmail.com')
        self.order = Order.objects.create(customer=self.customer)
    
    def test_order_retreive(self):
        """Test if order retreived successfully"""
        self.assertEqual(self.order.id, 1)
    
    def test_order_create(self):
        """Test if order created seccussfully"""
        new_order = Order.objects.create(customer=self.customer, price=20000)
        self.assertEqual(new_order.id, 2)

    def test_order_update(self):
        """Test if order updated seccussfully"""
        self.assertEqual(self.order.content, None)

        self.order.content = 'This is something'
        self.order.save()
        self.assertNotEqual(self.order.content, None)
    
    def test_order_delete(self):
        """Test if order deleted seccussfully"""
        self.assertTrue(Order.objects.filter(customer=self.customer).exists())

        Order.objects.filter(id=self.order.id).delete()
        self.assertFalse(Order.objects.filter(customer=self.customer).exists())
    

    def test_order_order_by_price(self):
        """Test if bunch of orders could be ordered by price"""
        order2 = Order.objects.create(customer=self.customer, price=decimal.Decimal(1000))
        print("order2: ", order2.id)
        order3 = Order.objects.create(customer=self.customer, price=decimal.Decimal(2000))
        print("order3: ", order3.id)
        order4 = Order.objects.create(customer=self.customer, price=decimal.Decimal(2000))
        print("order4: ", order4.id)
        order5 = Order.objects.create(customer=self.customer, price=decimal.Decimal(3000))
        print("order5: ", order5.id)
        order6 = Order.objects.create(customer=self.customer, price=decimal.Decimal(100))
        print("order6: ", order6.id)
        
        orders = Order.objects.all().order_by('-price')
        for order in orders:
            print(order, ",   price: ", order.price)
