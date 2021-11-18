""""Unit tests for Registration API"""
import unittest
import requests

def create_user(citizen_id, name, surname, birth_date, occupation, phone_number, is_risk, address):
    """Create new user for registration."""
    return {
        'citizen_id': citizen_id,
        'name': name, 
        'surname': surname, 
        'birth_date': birth_date, 
        'occupation': occupation, 
        'phone_number': phone_number, 
        'is_risk': is_risk,
        'address': address,
    }


class RegistrationAPITest(unittest.TestCase):

    def setUp(self):
        self.base_url = 'https://wcg-apis.herokuapp.com/registration'
        self.citizen_1 = create_user('1116789838901', 'Benjamin', 'Lee', '1999-05-17', 'bartender', '0817741235', 'False', 'Bangkok')
        requests.delete(f'{self.base_url}/1116789838901')

    def test_post_registration_with_correct_format(self):
        """Test registered with corrected format."""
        self.response = requests.post(self.base_url, params=self.citizen_1)
        self.assertEqual(self.response.json()['feedback'], "registration success!")
        self.assertEqual(self.response.status_code, 201)

    def test_post_already_register_person(self):
        """Test registered again with same citizen."""
        requests.post(self.base_url, params=self.citizen_1)
        self.response = requests.post(self.base_url, params=self.citizen_1)
        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(self.response.json()['feedback'], "registration failed: this person already registered")

    def test_post_registration_missing_citizen_id(self):
        """Test registered with missing citizen_id as param."""
        missing_id = self.citizen_1.pop('citizen_id', None)
        self.response = requests.post(self.base_url, params=missing_id)
        self.assertEqual(self.response.status_code, 400)

    def test_post_registration_non_13_digit_citizen_id(self):
        """Test registered with citizen_id that isn't 13 digits."""
        self.citizen_1['citizen_id'] = "1111"
        self.response = requests.post(self.base_url, params=self.citizen_1)
        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(self.response.json()['feedback'], "registration failed: invalid citizen ID")

    def test_post_registration_missing_name(self):
        """Test registered with missing name as param."""
        self.citizen_1.pop('name', None)
        self.response = requests.post(self.base_url, params=self.citizen_1)
        self.assertEqual(self.response.status_code, 400)
        

    def test_post_registration_using_integer_name(self):
        """Test registered using name that is integer."""
        self.citizen_1['name'] = 123
        self.response = requests.post(self.base_url, params=self.citizen_1)
        self.assertNotEqual(self.response.json()['feedback'], "registration success!")
        
    def test_post_registration_missing_surname(self):
        """Test registered with missing surname as param."""
        self.citizen_1.pop('surname', None)
        self.response = requests.post(self.base_url, params=self.citizen_1)
        self.assertEqual(self.response.status_code, 400)

    def test_post_registration_using_integer_surname(self):
        """Test registered using surname that is integer."""
        self.citizen_1['surname'] = 123
        self.response = requests.post(self.base_url, params=self.citizen_1)
        self.assertNotEqual(self.response.json()['feedback'], "registration success!")
       

    def test_post_registration_missing_birth_date(self):
        """Test registered with missing birth_date as param."""
        self.citizen_1.pop('birth_date', None)
        self.response = requests.post(self.base_url, params=self.citizen_1)
        self.assertEqual(self.response.status_code, 400)

    def test_post_registration_incorrect_birth_date_format(self):
        """Test registered using %Y-%d-% format for birth_date."""
        self.citizen_1['birth_date'] = '1999-17-05'
        self.response = requests.post(self.base_url, params=self.citizen_1)
        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(self.response.json()['feedback'], "registration failed: invalid birth date format")

    def test_post_registration_less_than_12_years_old(self):
        """Test registered with age less than 12 years old."""
        self.citizen_1['birth_date'] = '2018-05-17'
        self.response = requests.post(self.base_url, params=self.citizen_1)
        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(self.response.json()['feedback'], "registration failed: not archived minimum age")
   
    def test_post_registration_missing_occupation(self):
        """Test registered with missing occupation as param."""
        self.citizen_1.pop('occupation', None)
        self.response = requests.post(self.base_url, params=self.citizen_1)
        self.assertEqual(self.response.status_code, 400)


    def test_post_registration_missing_address(self):
        """Test registered with missing address as param."""
        self.citizen_1.pop('address', None)
        self.response = requests.post(self.base_url, params=self.citizen_1)
        self.assertEqual(self.response.status_code, 400)

    def test_post_registration_missing_phone_number(self):
        """Test registered with missing phone number as param."""
        self.citizen_1.pop('phone_number', None)
        self.response = requests.post(self.base_url, params=self.citizen_1)
        self.assertEqual(self.response.status_code, 400)
    
    def test_post_registration_string_phone_number(self):
        """Test registered with string phone number as param."""
        self.citizen_1['phone_number'] = 'abcdefghij'
        self.response = requests.post(self.base_url, params=self.citizen_1)
        self.assertNotEqual(self.response.json()['feedback'], "registration success!")

    def test_post_registration_non_10_digit_phone_number(self):
        """Test registered with phone number not 10 digits."""
        self.citizen_1['phone_number'] = "081"
        self.response = requests.post(self.base_url, params=self.citizen_1)
        self.assertNotEqual(self.response.json()['feedback'], "registration success!")


if __name__ == "__main__":
    unittest.main()
