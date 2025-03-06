from odoo.tests.common import TransactionCase, tagged, Form
from odoo.exceptions import UserError, ValidationError


@tagged('-standard', 'test_partner_uniqueness')
class TestResPartnerUniqueness(TransactionCase):

    def setUp(self):
        super(TestResPartnerUniqueness, self).setUp()
        # Create a company for testing
        self.company = self.env['res.partner'].create({
            'name': 'Test Company',
            'is_company': True,
        })

        # Create another company to test uniqueness within the same company
        self.other_company = self.env['res.partner'].create({
            'name': 'Other Company',
            'is_company': True,
        })

        # Create a person for testing
        self.person = self.env['res.partner'].create({
            'name': 'Test Person',
            'is_company': False,

        })

    def test_check_customer_uniqueness_company_br_number(self):
        # Create a company with a duplicate BR number in the same company
        self.env['res.partner'].create({
            'name': 'Duplicate Company',
            'is_company': True,
            'br_number': '123456',
        })

        # Create another company with the same BR number in the same company to test uniqueness
        duplicate_company = self.env['res.partner'].create({
            'name': 'Another Company',
            'is_company': True,
            'br_number': '123456',
        })

        # This should raise a UserError
        with self.assertRaises(UserError):
            duplicate_company._check_customer_uniqueness()

    def test_check_customer_uniqueness_company_name(self):
        # Create a company with a duplicate name in the same company
        self.env['res.partner'].create({
            'name': 'Duplicate Company Name',
            'is_company': True,
        })

        # Create another company with the same name in the same company to test uniqueness
        duplicate_company_name = self.env['res.partner'].create({
            'name': 'Duplicate Company Name',
            'is_company': True,
        })

        # This should raise a UserError
        with self.assertRaises(UserError):
            duplicate_company_name._check_customer_uniqueness()

    def test_check_customer_uniqueness_person_name(self):
        # Create a person with a duplicate name under the same parent and company
        self.env['res.partner'].create({
            'name': 'Duplicate Person Name',
        })

        # Create another person with the same name under the same parent and company to test uniqueness
        duplicate_person_name = self.env['res.partner'].create({
            'name': 'Duplicate Person Name',
            'company_type': 'person',
        })

        # This should raise a ValidationError
        with self.assertRaises(ValidationError):
            duplicate_person_name._check_customer_uniqueness()

    def test_check_customer_uniqueness_no_duplicates(self):
        # Create a company with unique BR number and name
        unique_company = self.env['res.partner'].create({
            'name': 'Unique Company',
            'is_company': True,
            'br_number': 'unique_br_number',
        })

        # This should not raise any errors
        unique_company._check_customer_uniqueness()

        # Create a person with a unique name
        unique_person = self.env['res.partner'].create({
            'name': 'Unique Person',
            'is_company': False,
        })

        # This should not raise any errors
        unique_person._check_customer_uniqueness()
