#!/usr/bin/env python3
# Author: Ryan Tiffany
# Copyright (c) 2024
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

__author__ = 'ryantiffany'
import os
import click
import json
from rich.console import Console
from rich.table import Table
from rich import box
from utils import SDKConnector
from ibm_cloud_sdk_core import ApiException

ibmcloud_api_key = os.environ.get('IBMCLOUD_API_KEY')
if not ibmcloud_api_key:
    raise ValueError("IBMCLOUD_API_KEY environment variable not found")

ibm_client = SDKConnector(ibmcloud_api_key)
tagging_service = ibm_client.create_global_tagging_service()

def get_all_tags():
    try:
        tag_list = tagging_service.list_tags(
          tag_type='user',
          attached_only=True,
          full_data=True,
          providers=['ghost,ims'],
          order_by_name='asc').get_result()
    except ApiException as e:
        print("Exception when calling GlobalTaggingV1: %s\n" % e)

    return tag_list  

def get_ghost_tags():
    try:
        tag_list = tagging_service.list_tags(
          tag_type='user',
          attached_only=True,
          full_data=True,
          providers=['ghost'],
          order_by_name='asc').get_result()
    except ApiException as e:
        print("Exception when calling GlobalTaggingV1: %s\n" % e)
    
    return tag_list

@click.command() 
@click.option('--all', default=None, help='Return all tags across ghost and ims backends. The default is to only return tags from the ghost backend.')
@click.option('--json', is_flag=True, help='Output as JSON')
def main(all, json):


    try:
      if all or json:
          tag_list = get_all_tags()
          if json:
              print(json.dumps(tag_list, indent=2))
          elif all:
              console = Console()
              table = Table(show_header=True, header_style="white", box=box.ROUNDED)
              table.add_column("Tag Name")
              table.add_column("Provider")
              table.add_column("Resources", justify="right")
              for tag in tag_list['items']:
                providers = ", ".join(sorted(tag.get('providers', [])))
                count = 0
                if 'attached_to_resources' in tag:
                  count = tag['attached_to_resources']['ghost']
                else:
                  count = "N/A"
                table.add_row(
                  tag['name'],
                  providers,
                  str(count)
                )
              console.print(table)
      else:
          tag_list = get_ghost_tags()
          console = Console()
          table = Table(show_header=True, header_style="white", box=box.ROUNDED)
          table.add_column("Tag Name")
          table.add_column("Resources", justify="right")
          for tag in tag_list['items']:
              providers = ", ".join(sorted(tag.get('providers', [])))
              count = 0
              if 'attached_to_resources' in tag:
                  count = tag['attached_to_resources']['ghost']
              else:
                  count = "N/A"
              table.add_row(
                  tag['name'],
                  providers,
                  str(count)
                )
          console.print(table)
    except ApiException as e:
        print("Exception when calling GlobalTaggingV1: %s\n" % e)


    # # if json:
    # #     data = []
    # # else:    
    # #     console = Console()
    # #     table = Table(show_header=True, header_style="white", box=box.ROUNDED)
    # #     table.add_column("Tag Name")
    # #     table.add_column("Provider")
    # #     table.add_column("Resources", justify="right")

    # try:
    #     if all:
    #         tag_list = get_all_tags()
    #     else:
    #         tag_list = get_ghost_tags()

    #     for tag in tag_list['items']:
        
    #       providers = ", ".join(sorted(tag.get('providers', [])))
          
    #       count = 0
    #       if 'attached_to_resources' in tag:
    #         count = tag['attached_to_resources']['ghost']
    #       else:
    #         count = "N/A"
        
    #       table.add_row(
    #         tag['name'],
    #         providers,
    #         str(count)
    #       )
        
    #     console.print(table)
    #     if json:
    #         tag_json = get_all_tags()
    #         print(json.dumps(tag_json, indent=2))
    # except ApiException as e:
    #     print("Exception when calling GlobalTaggingV1: %s\n" % e)

if __name__ == "__main__":
    main()
