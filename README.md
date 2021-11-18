# API-Testing
Test API of WCG group using registration endpoint based on this [API format](https://wcg-apis.herokuapp.com/document/registration)

Test date: 18/11/2021

Defect found:

1. Name can be integer value  like 123
2. Surname can be integer value  like 123
3. Phone number can be a string value like "abcdefghij"
4. Phone number can be any digits like 081

| Test case                                          | Expected Result                                                                           | Status |
|----------------------------------------------------|-------------------------------------------------------------------------------------------|--------|
| test_post_registration_with_correct_format         | return 201 Created and feedback responses registration success                            |    P   |
| test_post_already_register_person                  | return 200 OK with feedback responses registration failed: this person already registered |    P   |
| test_post_registration_missing_citizen_id          | return 400 Bad Request                                                                    |    P   |
| test_post_registration_non_13_digit_citizen_id     | return 200 OK with feedback responses registration failed: invalid citizen ID             |    P   |
| test_post_registration_missing_name                | return 400 Bad Request                                                                    |    P   |
| test_post_registration_using_integer_name          | should not return feedback responses registration success                                 |    F   |
| test_post_registration_missing_surname             | return 400 Bad Request                                                                    |    P   |
| test_post_registration_using_integer_surname       | should not return feedback responses registration success                                 |    F   |
| test_post_registration_missing_birth_date          | return 400 Bad Request                                                                    |    P   |
| test_post_registration_incorrect_birth_date_format | return 200 OK with feedback responses registration failed: invalid birth date format      |    P   |
| test_post_registration_less_than_12_years_old      | return 200 OK with feedback responses registration failed: not archived minimum age       |    P   |
| test_post_registration_missing_occupation          | return 400 Bad Request                                                                    |    P   |
| test_post_registration_missing_address             | return 400 Bad Request                                                                    |    P   |
| test_post_registration_string_phone_number         | should not return feedback responses registration success                                 |    F   |
| test_post_registration_non_10_digit_phone_number   | should not return feedback responses registration success                                 |    F   |