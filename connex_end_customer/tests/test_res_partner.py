from odoo.tests.common import TransactionCase, tagged
from odoo.exceptions import ValidationError

@tagged('-standard', 'test_br_number')
class TestResPartner(TransactionCase):

    def setUp(self):
        super(TestResPartner, self).setUp()
        # Create the company 'CONNEX 360 (PVT) LTD'
        self.connex_company = self.env['res.company'].create({
            'name': 'CONNEX 360 (PVT) LTD',
        })

        # Create a partner that is not 'CONNEX 360 (PVT) LTD'
        self.other_company = self.env['res.company'].create({
            'name': 'Other Company',
        })

    def test_check_br_number_valid(self):
        # Create a record with a BR Number for 'CONNEX 360 (PVT) LTD'
        partner = self.env['res.partner'].create({
            'name': 'Test Partner',
            'company_id': self.connex_company.id,
            'is_company': True,
            'br_number': '123456',
        })
        # This should not raise a ValidationError
        partner._check_br_number()

    def test_check_br_number_missing_br_number(self):
        # Create a record with no BR Number for 'CONNEX 360 (PVT) LTD'
        partner = self.env['res.partner'].create({
            'name': 'Test Partner No BR',
            'company_id': self.connex_company.id,
            'company_type': 'company',
        })
        # This should raise a ValidationError
        with self.assertRaises(ValidationError):
            partner._check_br_number()

    def test_check_br_number_other_company(self):
        # Create a record for another company that should not require a BR Number
        partner = self.env['res.partner'].create({
            'name': 'Test Partner Other Company',
            'company_id': self.other_company.id,
            'company_type': 'company',
        })
        # This should not raise a ValidationError
        partner._check_br_number()
