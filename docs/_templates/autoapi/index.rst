API Reference
=============

This page contains auto-generated API reference documentation [#f1]_.

.. toctree::
   :titlesonly:

   {% for page in pages|selectattr("is_top_level_object") %}
   {{ page.include_path }}
   {% endfor %}

   {# XXX: resolve what to do / reference
      https://github.com/readthedocs/sphinx-autoapi/issues/298
   #}

   {% for page in pages | sort %}
   {#
      Add the top most levels in "astronomer.providers.X" to the index file
      This is needed because we don't have __init__.py file in astronomer
      and astronomer/providers package as we use nested implicit namespace packages.
   #}
   {% if (page.top_level_object or page.name.split('.') | length == 3) and page.display %}
   {{ page.include_path }}
   {# {{ page.short_name | capitalize }} <{{ page.include_path }}> #}
   {% endif %}
   {% endfor %}

.. [#f1] Created with `sphinx-autoapi <https://github.com/readthedocs/sphinx-autoapi>`_
