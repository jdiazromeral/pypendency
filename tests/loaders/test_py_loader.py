import os
from unittest import TestCase

from pypendency.builder import ContainerBuilder
from pypendency.loaders import exceptions
from pypendency.loaders.py_loader import PyLoader
from tests.resources.class_a import A
from tests.resources.class_b import B
from tests.resources.class_c import C


class TestPyLoader(TestCase):
    def setUp(self) -> None:
        self._container_builder = ContainerBuilder([])
        self.loader = PyLoader(self._container_builder)
        self.current_dir = os.path.dirname(__file__)

    def test_load_fails_for_non_absolute_path(self):
        with self.assertRaises(exceptions.PathNotAbsolute):
            self.loader.load("relative/path")

    def test_load_fails_for_non_existing_file(self):
        with self.assertRaises(exceptions.ResourceNotFound):
            self.loader.load("/non/existing/path")

    def test_load_fails_for_loader_without_load_method(self):
        path = os.path.join(self.current_dir, "..", "resources", "test_di_no_load_method.py")
        with self.assertRaises(exceptions.MissingLoaderMethod):
            self.loader.load(path)

    def test_load_works_as_expected(self):
        path = os.path.join(self.current_dir, "..", "resources", "test_di.py")
        self.loader.load(path)
        c = self._container_builder.get("example.C")
        self.assertIsInstance(c, C)
        self.assertIsInstance(c.b, B)
        self.assertIsInstance(c.a, A)

    def test_load_by_module_name_fails_for_non_existing_file(self):
        with self.assertRaises(exceptions.ResourceNotFound):
            self.loader.load_by_module_name("nonexistingpath")

    def test_load_by_module_name_fails_for_loader_without_load_method(self):
        with self.assertRaises(exceptions.MissingLoaderMethod):
            self.loader.load_by_module_name("tests.resources.test_di_no_load_method")

    def test_load_by_module_name_fails_for_module_with_generic_attribute_error(self):
        with self.assertRaises(AttributeError):
            self.loader.load_by_module_name("tests.resources.test_di_with_generic_attribute_error")

    def test_load_by_module_name_works_as_expected(self):
        self.loader.load_by_module_name("tests.resources.test_di")
        c = self._container_builder.get("example.C")
        self.assertIsInstance(c, C)
        self.assertIsInstance(c.b, B)
        self.assertIsInstance(c.a, A)

    def test_load_dir(self):
        path = os.path.join(self.current_dir, "..", "resources", "loaders")
        self.loader.load_dir(path)
        self.assertIsInstance(self._container_builder.get("same_level_file"), A)
        self.assertIsInstance(self._container_builder.get("one_level_file"), A)
        self.assertIsInstance(self._container_builder.get("two_levels_file"), A)

    def test_load_dir_fails_for_non_absolute_path(self):
        with self.assertRaises(exceptions.PathNotAbsolute):
            self.loader.load_dir("tests/resources/loaders")
