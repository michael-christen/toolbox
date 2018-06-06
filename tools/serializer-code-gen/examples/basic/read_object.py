import imp
import os
import sys


def get_module_objects(filepath=None):
    """Return all public objects defined at filepath.

    That includes class definitions.
    """
    CUSTOM_MODULE_LOADER_NAME = 'serializer-code-gen_module_loader'
    try:
        if filepath:
            mod = imp.load_source(CUSTOM_MODULE_LOADER_NAME, filepath)
        else:
            mod = imp.load_source(CUSTOM_MODULE_LOADER_NAME, 'fake_filepath.py',
                                  sys.stdin)
    except ValueError as exc:
        if 'relative import' in str(exc):
            raise NotImplementedError(
                "We don't support relative imports from source packages")
        raise
    module_objects = []
    for mod_attr in dir(mod):
        if not mod_attr.startswith('_'):
            obj = getattr(mod, mod_attr)
            obj_module = getattr(obj, '__module__', None)
            if obj_module == CUSTOM_MODULE_LOADER_NAME:
                module_objects.append(obj)
    return module_objects


def custom_setup():
    """Provide any necessary configuration before loading modules.
    """
    # Make sure DRF/Django doesn't complain about DJANGO_SETTINGS_MODULE not
    # being defined
    django_settings = os.environ.get('DJANGO_SETTINGS_MODULE')
    if not django_settings:
        os.environ['DJANGO_SETTINGS_MODULE'] = 'fake_settings'


def main():
    custom_setup()
    objects = get_module_objects()
    print objects



if __name__ == '__main__':
    main()
