import sublime, sublime_plugin
import os

class rungiboCommand(sublime_plugin.WindowCommand):

	_bp_list = []
	_package_path = ''

	def find_path(self):
		if not self._package_path:
			paths = [os.path.join(sublime.installed_packages_path(), 'Gitignore.sublime-package'),
					os.path.join(sublime.packages_path(), 'Gitignore'),
					os.path.join(sublime.packages_path(), 'Sublime-Gitignore')]
			for path in paths:
				print("Trying path: " + path);
				try:
					sublime.load_resource(os.path.join(path, 'boilerplates.json'))
					self._package_path = path
				except:
					continue;

		print("Found path: " + self._package_path)
		return self._package_path

	def build_list(self):
		if not self._bp_list:
			path = self.find_path();

			for dir in os.listdir(path):
				self._bp_list.append(dir.replace('.gitignore', ''))

		self.chosen_array = []
		self.first_list = self._bp_list[:]	# Copy _bp_list
		self.second_list = ['Done'] + self._bp_list

	def show_quick_panel(self, options, done):
		# Fix from
		# http://www.sublimetext.com/forum/viewtopic.php?f=6&t=10999
		sublime.set_timeout(lambda: self.window.show_quick_panel(options, done), 10)

	def run(self):
		self.build_list()
		self.show_quick_panel(self.first_list, self.first_select)

	def first_select(self, index):
		if index > -1:
			self.chosen_array.append(self.first_list[index])
			self.second_list.remove(self.first_list[index])
			self.show_quick_panel(self.second_list, self.second_select)

	def second_select(self, index):
		if index == 0:
			self.write_file()
			self.build_list()
		elif index > 0:
			self.chosen_array.append(self.second_list[index])
			self.second_list.remove(self.second_list[index])
			self.show_quick_panel(self.second_list, self.second_select)

	def write_file(self):
		path = self.find_path();

		final = ''

		for bp in self.chosen_array:
			bpfile = open(path + bp + '.gitignore', 'r')
			text = bpfile.read()
			bpfile.close()

			final = final + '###' + bp + '###\n \n' + text + '\n\n'

		view = sublime.active_window().new_file()
		view.run_command('writegibo', {'bp': final})


class writegiboCommand(sublime_plugin.TextCommand):

	def run(self, edit, **kwargs):
		self.view.insert(edit, 0, kwargs['bp'])
		self.view.set_name('.gitignore')
		self.view.end_edit(edit)
