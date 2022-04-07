from typing import Any, Iterable, List, Mapping, MutableMapping, Optional, Tuple

import requests
from airbyte_cdk import AirbyteLogger
from airbyte_cdk.sources import AbstractSource
from airbyte_cdk.sources.streams import Stream
from airbyte_cdk.sources.streams.http import HttpStream
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient


from . import pokemon_list

#class SourcePythonHttpExample(AbstractSource):
class SourceHydrovu(AbstractSource):
    
    def check_connection(self, logger, config) -> Tuple[bool, any]:
        print ('config["client_secret"]')
        print (config["client_secret"])
        print ('config["account_id"]')
        print (config["account_id"])
        input_pokemon = config["pokemon_name"]

        # create session
        client = BackendApplicationClient(client_id=config["account_id"])
        oauth = OAuth2Session(client=client)
        token = oauth.fetch_token(token_url='https://www.hydrovu.com/public-api/oauth/token', client_id=config["account_id"], client_secret=config["client_secret"])

        # get list of locations
        r = oauth.get('https://www.hydrovu.com/public-api/v1/locations/list')
        locations = r.json()

        print ("locations")
        print (locations)



        if input_pokemon not in pokemon_list.POKEMON_LIST:
            return False, f"Input Pokemon {input_pokemon} is invalid. Please check your spelling and input a valid Pokemon."
        else:
            return True, None
    
        '''
    def check_connection(self, logger: AirbyteLogger, config: Mapping[str, Any]) -> Tuple[bool, any]:

        try:
            #stripe.api_key = config["client_secret"]
            #stripe.Account.retrieve(config["account_id"])

            print ('config["client_secret"]')
            print (config["client_secret"])

            return True, None
        except Exception as e:
            return False, e
        '''


        '''
        input_pokemon = config["pokemon_name"]
        if input_pokemon not in pokemon_list.POKEMON_LIST:
            return False, f"Input Pokemon {input_pokemon} is invalid. Please check your spelling and input a valid Pokemon."
        else:
            return True, None
        '''


    def streams(self, config: Mapping[str, Any]) -> List[Stream]:
        return [Pokemon(pokemon_name=config["pokemon_name"])]


class Pokemon(HttpStream):
    url_base = "https://pokeapi.co/api/v2/"

    # Set this as a noop.
    primary_key = None

    def __init__(self, pokemon_name: str, **kwargs):
        super().__init__(**kwargs)
        # Here's where we set the variable from our input to pass it down to the source.
        self.pokemon_name = pokemon_name

    def path(self, **kwargs) -> str:
        pokemon_name = self.pokemon_name
        # This defines the path to the endpoint that we want to hit.
        return f"pokemon/{pokemon_name}"

    def request_params(
            self,
            stream_state: Mapping[str, Any],
            stream_slice: Mapping[str, Any] = None,
            next_page_token: Mapping[str, Any] = None,
    ) -> MutableMapping[str, Any]:
        # The api requires that we include the Pokemon name as a query param so we do that in this method.
        return {"pokemon_name": self.pokemon_name}

    def parse_response(
            self,
            response: requests.Response,
            stream_state: Mapping[str, Any],
            stream_slice: Mapping[str, Any] = None,
            next_page_token: Mapping[str, Any] = None,
    ) -> Iterable[Mapping]:
        # The response is a simple JSON whose schema matches our stream's schema exactly,
        # so we just return a list containing the response.
        return [response.json()]

    def next_page_token(self, response: requests.Response) -> Optional[Mapping[str, Any]]:
        # While the PokeAPI does offer pagination, we will only ever retrieve one Pokemon with this implementation,
        # so we just return None to indicate that there will never be any more pages in the response.
        return None
