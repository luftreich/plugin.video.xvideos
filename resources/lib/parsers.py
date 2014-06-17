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
import HTMLParser
from xbmcutil import listitem, plugin

# Host Url
host = u"http://www.xvideos.com%s"

class VideoParser(HTMLParser.HTMLParser):
	"""
		Parses available episods for current show, i.e from http://www.xvideos.com/new/0/
	"""
	
	def parse(self, html):
		""" Parses SourceCode and Scrape Episodes """
		
		# Class Vars
		self.counter = (int(plugin.get("NextPageCount",1)) -1) * 20
		self.divcount = None
		self.section = 0
		
		# Proceed with parsing
		results = []
		self.reset_lists()
		self.append = results.append
		try: self.feed(html)
		except plugin.ParserError: pass
		
		# Return Results
		return results
	
	def reset_lists(self):
		# Reset List for Next Run
		self.item = listitem.ListItem()
		self.item.setAudioInfo()
		self.item.setQualityIcon(False)
		self.item.urlParams["action"] = "PlayVideo"
	
	def handle_starttag(self, tag, attrs):
		# Convert Attributes to a Dictionary
		if self.divcount == 0:
			self.append(listitem.ListItem.add_next_page())
			raise plugin.ParserError
		elif attrs:
			# Find show-block elements and all div sub elements
			if tag == u"div":
				# Increment div counter when within show-block
				if self.divcount: self.divcount +=1
				else:
					# Convert Attributes to a Dictionary
					attrs = dict(attrs)
					
					# Check for required section
					if u"id" in attrs and attrs[u"id"] == u"content": self.divcount = 1
			
			# When within show-block fetch show data
			if self.divcount >= 4:
				# Convert Attributes to a Dictionary
				attrs = dict(attrs)
				
				# Fetch Video url and Video Runtime
				if self.divcount == 4:
					# Fetch Video Url
					if tag == u"a" and u"href" in attrs:
						url = host % attrs[u"href"]
						self.item.urlParams["url"] = url
						self.item.addRelatedContext(url=url)
						self.section = 101
					
					# Fetch Video runtime
					elif tag == u"span" and u"class" in attrs and attrs[u"class"] == u"duration":
						self.section = 102
				
				# Fetch Image url
				elif self.divcount == 5:
					if tag == u"img" and u"src" in attrs:
						self.item.setThumbnailImage(attrs[u"src"])
	
	def handle_data(self, data):
		# Fetch Title
		if self.section == 101:
			self.counter += 1
			data = data.strip()
			if data: self.item.setLabel("%i. %s" % (self.counter, data.title()))
			else: self.item.setLabel("%i. No Name" % (self.counter))
			self.section = 0
		
		# Fetch Duration
		elif self.section == 102:
			duration = 0
			for num, types in (part.split("-") for part in data.replace("h","-h").replace(" min","-min").replace(" sec","-sec")[1:-1].split(" ")):
				num = int(num)
				if types == "h": duration += (num * 3600)
				elif types == "min": duration += (num * 60)
				else: duration += num
			
			self.item.setDurationInfo(duration)
			self.section = 0
	
	def handle_endtag(self, tag):
		# Decrease div counter on all closing div elements
		if tag == u"div" and self.divcount:
			self.divcount -= 1
			
			# When at closeing tag for show-block, save fetched data
			if self.divcount == 3:
				if self.item.getLabel(): self.append(self.item.getListitemTuple(True))
				self.reset_lists()

class Related(HTMLParser.HTMLParser):
	"""
		Parses available episods for current show, i.e from http://www.xvideos.com/video6672732/teen_foot_and_fist_fucking_penetrations
	"""
	
	def parse(self, html):
		""" Parses SourceCode and Scrape Episodes """
		
		# Class Vars
		self.counter = (int(plugin.get("NextPageCount",1)) -1) * 25
		self.divcount = None
		self.section = 0
		
		# Proceed with parsing
		results = []
		self.reset_lists()
		self.append = results.append
		try: self.feed(html)
		except plugin.ParserError: pass
		
		# Return Results
		return results
	
	def reset_lists(self):
		# Reset List for Next Run
		self.item = listitem.ListItem()
		self.item.setAudioInfo()
		self.item.setQualityIcon(False)
		self.item.urlParams["action"] = "system.source"
	
	def handle_starttag(self, tag, attrs):
		# Convert Attributes to a Dictionary
		if self.divcount == 0:
			self.append(listitem.ListItem.add_next_page())
			raise plugin.ParserError
		elif attrs:
			# Find show-block elements and all div sub elements
			if tag == u"div":
				# Increment div counter when within show-block
				if self.divcount: self.divcount +=1
				else:
					# Convert Attributes to a Dictionary
					attrs = dict(attrs)
					
					# Check for required section
					if u"id" in attrs and attrs[u"id"] == u"content": self.divcount = 1
			
			# When within show-block fetch show data
			if self.divcount >= 4:
				# Convert Attributes to a Dictionary
				attrs = dict(attrs)
				
				# Fetch Video url and Video Runtime
				if self.divcount == 4:
					# Fetch Video Url
					if tag == u"a" and u"href" in attrs:
						url = host % attrs[u"href"]
						self.item.urlParams["url"] = url
						self.item.addRelatedContext(url=url)
						self.section = 101
					
					# Fetch Video runtime
					elif tag == u"span" and u"class" in attrs and attrs[u"class"] == u"duration":
						self.section = 102
				
				# Fetch Image url
				elif self.divcount == 5:
					if tag == u"img" and u"src" in attrs:
						self.item.setThumbnailImage(attrs[u"src"])
	
	def handle_data(self, data):
		# Fetch Title
		if self.section == 101:
			self.counter += 1
			data = data.strip()
			if data: self.item.setLabel("%i. %s" % (self.counter, data.title()))
			else: self.item.setLabel("%i. No Name" % (self.counter))
			self.section = 0
		
		# Fetch Duration
		elif self.section == 102:
			duration = 0
			for num, types in (part.split("-") for part in data.replace("h","-h").replace(" min","-min").replace(" sec","-sec")[1:-1].split(" ")):
				num = int(num)
				if types == "h": duration += (num * 3600)
				elif types == "min": duration += (num * 60)
				else: duration += num
			
			self.item.setDurationInfo(duration)
			self.section = 0
	
	def handle_endtag(self, tag):
		# Decrease div counter on all closing div elements
		if tag == u"div" and self.divcount:
			self.divcount -= 1
			
			# When at closeing tag for show-block, save fetched data
			if self.divcount == 3:
				self.append(self.item.getListitemTuple(True))
				self.reset_lists()