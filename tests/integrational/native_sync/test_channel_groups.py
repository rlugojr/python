import unittest
import logging
import pubnub
import time

from pubnub.models.consumer.channel_group import PNChannelGroupsAddChannelResult, PNChannelGroupsListResult, \
    PNChannelGroupsRemoveChannelResult, PNChannelGroupsRemoveGroupResult
from pubnub.pubnub import PubNub
from tests.helper import pnconf_copy, use_cassette_and_stub_time_sleep

pubnub.set_stream_logger('pubnub', logging.DEBUG)


class TestPubNubChannelGroups(unittest.TestCase):
    @use_cassette_and_stub_time_sleep('tests/integrational/fixtures/channel_groups/single_channel.yaml',
                                      filter_query_parameters=['uuid'])
    def test_single_channel(self):
        ch = "herenow-unit-ch"
        gr = "herenow-unit-cg"
        pubnub = PubNub(pnconf_copy())

        # add
        result = pubnub.add_channel_to_channel_group() \
            .channels(ch) \
            .channel_group(gr) \
            .sync()

        assert isinstance(result, PNChannelGroupsAddChannelResult)

        time.sleep(2)

        # list
        result = pubnub.list_channels_in_channel_group() \
            .channel_group(gr) \
            .sync()

        assert isinstance(result, PNChannelGroupsListResult)
        assert len(result.channels) == 1
        assert result.channels[0] == ch

        # remove
        result = pubnub.remove_channel_from_channel_group() \
            .channels(ch) \
            .channel_group(gr) \
            .sync()

        assert isinstance(result, PNChannelGroupsRemoveChannelResult)

        time.sleep(2)

        # list
        result = pubnub.list_channels_in_channel_group() \
            .channel_group(gr) \
            .sync()

        assert isinstance(result, PNChannelGroupsListResult)
        assert len(result.channels) == 0

    @use_cassette_and_stub_time_sleep(
        'tests/integrational/fixtures/channel_groups/add_remove_multiple_channels.yaml',
        filter_query_parameters=['uuid'])
    def test_add_remove_multiple_channels(self):
        ch1 = "herenow-unit-ch1"
        ch2 = "herenow-unit-ch2"
        gr = "herenow-unit-cg"
        pubnub = PubNub(pnconf_copy())

        # add
        result = pubnub.add_channel_to_channel_group() \
            .channels([ch1, ch2]) \
            .channel_group(gr) \
            .sync()

        assert isinstance(result, PNChannelGroupsAddChannelResult)

        time.sleep(1)

        # list
        result = pubnub.list_channels_in_channel_group() \
            .channel_group(gr) \
            .sync()

        assert isinstance(result, PNChannelGroupsListResult)
        assert len(result.channels) == 2
        assert ch1 in result.channels
        assert ch2 in result.channels

        # remove
        result = pubnub.remove_channel_from_channel_group() \
            .channels([ch1, ch2]) \
            .channel_group(gr) \
            .sync()

        assert isinstance(result, PNChannelGroupsRemoveChannelResult)

        time.sleep(1)

        # list
        result = pubnub.list_channels_in_channel_group() \
            .channel_group(gr) \
            .sync()

        assert isinstance(result, PNChannelGroupsListResult)
        assert len(result.channels) == 0

    @use_cassette_and_stub_time_sleep(
        'tests/integrational/fixtures/channel_groups/add_channel_remove_group.yaml',
        filter_query_parameters=['uuid'])
    def test_add_channel_remove_group(self):
        ch = "herenow-unit-ch"
        gr = "herenow-unit-cg"
        pubnub = PubNub(pnconf_copy())

        # add
        result = pubnub.add_channel_to_channel_group() \
            .channels(ch) \
            .channel_group(gr) \
            .sync()

        assert isinstance(result, PNChannelGroupsAddChannelResult)

        time.sleep(1)

        # list
        result = pubnub.list_channels_in_channel_group() \
            .channel_group(gr) \
            .sync()

        assert isinstance(result, PNChannelGroupsListResult)
        assert len(result.channels) == 1
        assert result.channels[0] == ch

        # remove
        result = pubnub.remove_channel_group() \
            .channel_group(gr) \
            .sync()

        assert isinstance(result, PNChannelGroupsRemoveGroupResult)

        time.sleep(1)

        # list
        result = pubnub.list_channels_in_channel_group() \
            .channel_group(gr) \
            .sync()

        assert isinstance(result, PNChannelGroupsListResult)
        assert len(result.channels) == 0
