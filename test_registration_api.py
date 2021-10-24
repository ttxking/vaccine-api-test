""""Unit tests for Registration API"""
import unittest
import requests
import requests_mock
import re
from unittest.mock import Mock



def get_api(remove_param,replace):
    URL = "https://wcg-apis.herokuapp.com/registration?citizen_id=1116789838901&name=Benjamin&surname=Lee&birth_date=1999-05-17&occupation=bartender&address=Bangkok"
    if replace == "":
        if re.search(f"{remove_param}(.*?)&", URL):
            new_URL = re.sub(f"{remove_param}(.*?)&", "", URL)
        else:
            new_URL = re.sub(f"{remove_param}(.*?)", "", URL)
    else:
        if re.search(f"{remove_param}(.*?)&", URL):
            new_URL = re.sub(f"{remove_param}(.*?)&", f"{remove_param}={replace}&", URL)
        else:
            new_URL = re.sub(f"{remove_param}(.*?)", f"{remove_param}={replace}", URL)
    return new_URL

def post_registration():
    """Posting registration for mock"""
    response = requests.post(
        'https://wcg-apis.herokuapp.com/registration?citizen_id=1116789838901&name=Benjamin&surname=Lee&birth_date=1999-05-17&occupation=bartender&address=Bangkok')
    return response


class RegistrationAPITest(unittest.TestCase):

    def test_get_registration(self):
        """Test registration can be retrieved from the request."""
        self.response = requests.get(
            "https://wcg-apis.herokuapp.com/registration")
        self.assertEqual(self.response.status_code, 200)

    def test_post_registration_with_correct_format(self):
        """Test registered with corrected format using mock request_mock."""
        return_value = {
            "feedback": "registration success!"}  # Set return value for mock
        # This is because successful registration added real object into
        # database when we rerun test the test show user already registered
        # instead.
        with requests_mock.Mocker() as rm:
            rm.post(
                'https://wcg-apis.herokuapp.com/registration?citizen_id=1116789838901&name=Benjamin&surname=Lee&birth_date=1999-05-17&occupation=bartender&address=Bangkok',
                json=return_value,
                status_code=200)
            response = post_registration()

        self.assertEqual(
            response.json(), {
                "feedback": "registration success!"})
        self.assertEqual(response.status_code, 200)

    def test_post_registration_missing_citizen_id(self):
        """Test registered with missing citizen_id as query param."""
        self.response = requests.post(get_api(remove_param="citizen_id",replace=""))
        self.assertEqual(self.response.status_code, 400)

    def test_post_registration_non_13_digit_citizen_id(self):
        """Test registered with citizen_id that isn't 13 digits."""
        self.response = requests.post(get_api(remove_param="citizen_id", replace=1111))
        self.assertEqual(self.response.status_code, 200)
        self.assertEqual({
            "feedback": "registration failed: invalid citizen ID"
        }, self.response.json())

    def test_post_registration_missing_name(self):
        """Test registered with missing name as query param."""
        self.response = requests.post(get_api(remove_param="name", replace=""))
        self.assertEqual(self.response.status_code, 400)
        

    def test_post_registration_using_integer_name(self):
        """Test registered using name that is integer."""
        self.response = requests.post(get_api(remove_param="name", replace="123"))
        with self.assertRaises(TypeError):
            self.response
        self.assertEqual(self.response.status_code, 400)
        

    def test_post_registration_missing_surname(self):
        """Test registered with missing surname as query param."""
        self.response = requests.post(get_api(remove_param="surname", replace=""))
        self.assertEqual(self.response.status_code, 400)

    def test_post_registration_using_integer_surname(self):
        """Test registered using surname that is integer."""
        self.response = requests.post(get_api(remove_param="surname", replace="123"))
        with self.assertRaises(TypeError):
            self.response
        self.assertEqual(self.response.status_code, 400)

    def test_post_registration_missing_birth_date(self):
        """Test registered with missing birth_date as query param."""
        self.response = requests.post(get_api(remove_param="birth_date", replace=""))
        self.assertEqual(self.response.status_code, 400)

    def test_post_registration_incorrect_birth_date_format(self):
        """Test registered using %Y-%d-% format for birth_date."""
        # this have to be full URL to use different person
        self.response = requests.post(
            "https://wcg-apis.herokuapp.com/registration?citizen_id=1116789838110&name=Benedict&surname=Tan&birth_date=1999-17-05&occupation=bartender&address=Bangkok")
        self.assertEqual(self.response.status_code, 200)
        self.assertEqual({
            "feedback": "registration failed: invalid birth date format"
        }, self.response.json())

    def test_post_registration_less_than_12_years_old(self):
        """Test registered with age less than 12 years old."""
        # this have to be full URL to use different person
        self.response = requests.post(
            "https://wcg-apis.herokuapp.com/registration?citizen_id=1116789838110&name=Benedict&surname=Tan&birth_date=2018-05-17&occupation=bartender&address=Bangkok")
        self.assertEqual(self.response.status_code, 200)
        self.assertEqual({
            "feedback": "registration failed: not archived minimum age"
        }, self.response.json())

    def test_post_registration_missing_occupation(self):
        """Test registered with missing occupation as query param."""
        self.response = requests.post(get_api(remove_param="occupation", replace=""))
        self.assertEqual(self.response.status_code, 400)

    def test_post_registration_missing_address(self):
        """Test registered with missing address as query param."""
        self.response = requests.post(get_api(remove_param="address", replace=""))
        self.assertEqual(self.response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
