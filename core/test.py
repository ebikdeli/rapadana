from django.test import TestCase, Client

from .models import Customer, Order


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
