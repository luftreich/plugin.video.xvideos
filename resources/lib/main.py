"""
	Copyright: (c) 2013 William Forde (willforde+xbmc@gmail.com)
	License: GPLv3, see LICENSE for more details
	
	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.
	
	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.
	
	You should have received a copy of the GNU General Public License
	along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

# Call Necessary Imports
from xbmcutil import urlhandler, listitem, plugin
import parsers

class Initialize(listitem.VirtualFS):
	@plugin.error_handler
	def scraper(self):
		# Fetch Video Content
		url = u"http://www.xvideos.com/new/%i/" % (int(plugin.get("nextpagecount", 1))-1)
		sourceObj = urlhandler.urlopen(url, 3600) # TTL = 1 Hour
		videoItems = parsers.VideoParser().parse(sourceObj)
		sourceObj.close()
		
		# Set Content Properties
		self.set_sort_methods(self.sort_method_label, self.sort_method_video_runtime)
		self.set_content("episodes")
		
		# Return List of Video Listitems
		return videoItems

class Related(listitem.VirtualFS):
	@plugin.error_handler
	def scraper(self):
		# Fetch Video Content
		sourceObj = urlhandler.urlopen(plugin["url"], 14400) # TTL = 4 Hour
		videoItems = parsers.Related().parse(sourceObj)
		sourceObj.close()
		
		# Set Content Properties
		self.set_sort_methods(self.sort_method_label, self.sort_method_video_runtime)
		self.set_content("episodes")
		
		# Return List of Video Listitems
		return videoItems

class PlayVideo(listitem.PlayMedia):
	@plugin.error_handler
	def resolve(self):
		# Create url for oembed api
		sourceCode = urlhandler.urlread(plugin["url"], 14400, stripEntity=False) # TTL = 4 Hours
		
		# Search sourceCode
		import re
		VideoUrl = re.findall('flv_url=(http\S+?)&', sourceCode)[0]
		
		# Return Dict with Url or list of urls
		return {"url":plugin.urllib.unquote_plus(VideoUrl)}
