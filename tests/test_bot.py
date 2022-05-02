from unittest import mock
import pytest
import os

from multidrugs_bot import *

class TestTweetDataDrugs:

    @pytest.fixture(scope="function")
    def dummy_drug(self):
        return Drugs()

    def test_get_warning(self, dummy_drug):
        assert dummy_drug.get_warning() == True

    def test_get_description(self, dummy_drug):
        assert dummy_drug.get_description() == "Sorry, the format is not correct."

    def test_get_rxcui_1(self, dummy_drug):
        assert dummy_drug.get_rxcui_1() == ""

    def test_get_rxcui_2(self, dummy_drug):
        assert dummy_drug.get_rxcui_2() == ""

    def test_get_drug_name_1(self, dummy_drug):
        assert dummy_drug.get_drug_name_1() == ""

    def test_get_drug_name_2(self, dummy_drug):
        assert dummy_drug.get_drug_name_2() == ""

    def test_tweet_to_data_right(self, dummy_drug):
        dummy_drug.tweet_to_data("@multidrug aspirin ibuprofen")
        assert dummy_drug.get_drug_name_1() == "aspirin"
        assert dummy_drug.get_drug_name_2() == "ibuprofen"

    def test_tweet_to_data_multiple_input(self, dummy_drug):
        dummy_drug.tweet_to_data("@multidrug aspirin ibuprofen other drugs")
        assert dummy_drug.get_warning() == False
        assert dummy_drug.get_description() == "Sorry, the format is not correct."

    def test_tweet_to_data_single_input(self, dummy_drug):
        dummy_drug.tweet_to_data("@multidrug aspirin")
        assert dummy_drug.get_warning() == False
        assert dummy_drug.get_description() == "Sorry, the format is not correct."

    def test_tweet_to_data_single_no_input(self, dummy_drug):
        dummy_drug.tweet_to_data("@multidrug")
        assert dummy_drug.get_warning() == False
        assert dummy_drug.get_description() == "Sorry, the format is not correct."






