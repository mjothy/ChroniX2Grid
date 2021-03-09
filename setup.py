from setuptools import setup, find_packages


setup(name='Chronix2Grid',
      version='0.1.0rc10',
      description='A python package to generate "en-masse" chronics for loads and productions (thermal, renewable)',
      long_description='TODO',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
          "Intended Audience :: Developers",
          "Intended Audience :: Education",
          "Intended Audience :: Science/Research",
          "Natural Language :: English"
      ],
      keywords='ML powergrid optmization RL power-systems chronics generation production load network',
      author='Mario Jothy, Nicolas Megel, Vincent Renault',
      author_email=' mario.jothy@artelys.com',
      url="https://github.com/mjothy/chronix2grid",
      license='Mozilla Public License 2.0 (MPL 2.0)',
      packages=find_packages(),
      include_package_data=True,
      install_requires=["appdirs==1.4.3",
                        "attrs==19.3.0",
                        "backcall==0.1.0",
                        "bleach==3.1.1",
                        "branca==0.4.0",
                        "certifi==2019.11.28",
                        "chardet==3.0.4",
                        "click==7.1.1",
                        "colorama==0.4.3",
                        "colorlover==0.3.0",
                        "cufflinks==0.17.3",
                        "cycler==0.10.0",
                        "decorator==4.4.2",
                        "defusedxml==0.6.0",
                        "entrypoints==0.3",
                        "folium==0.10.1",
                        "Grid2Op==0.9.4",
                        "h5pyd==0.7.1",
                        "idna==2.9",
                        "importlib-metadata==1.5.0",
                        "ipykernel==5.1.4",
                        "ipython==7.13.0",
                        "ipython-genutils==0.2.0",
                        "ipywidgets==7.5.1",
                        "jedi==0.16.0",
                        "Jinja2==2.11.1",
                        "json5==0.9.3",
                        "jsonschema==3.2.0",
                        "jupyter==1.0.0",
                        "jupyter-client==6.0.0",
                        "jupyter-console==6.1.0",
                        "jupyter-core==4.6.3",
                        "jupyter-server==0.2.1",
                        "jupyterlab==2.0.1",
                        "jupyterlab-server==1.0.7",
                        "kiwisolver==1.1.0",
                        "llvmlite==0.31.0",
                        "MarkupSafe==1.1.1",
                        "matplotlib==3.1.3",
                        "mistune==0.8.4",
                        "nbconvert==5.6.1",
                        "nbformat==5.0.4",
                        "networkx==2.4",
                        "nose==1.3.7",
                        "notebook==6.0.3",
                        "numba==0.48.0",
                        "numexpr==2.7.1",
                        "packaging==20.3",
                        "pandapower==2.2.2",
                        "pandas==1.0.3",
                        "pandocfilters==1.4.2",
                        "parso==0.6.2",
                        "pathlib==1.0.1",
                        "pickleshare==0.7.5",
                        "plotly==4.5.2",
                        "ply==3.11",
                        "prometheus-client==0.7.1",
                        "prompt-toolkit==3.0.3",
                        "Pygments==2.5.2",
                        "Pyomo==5.6.8",
                        "pyparsing==2.4.6",
                        "pypsa==0.17.0",
                        "pyrsistent==0.15.7",
                        "pytest==6.2.2",
                        "pytest-tornasync==0.6.0.post2",
                        "python-dateutil==2.8.1",
                        "pytz==2019.3",
                        "PyUtilib==5.7.3",
                        "pyzmq==19.0.0",
                        "qtconsole==4.7.1",
                        "QtPy==1.9.0",
                        "requests==2.23.0",
                        "retrying==1.3.3",
                        "scipy==1.4.1",
                        "seaborn==0.10.0",
                        "Send2Trash==1.5.0",
                        "six==1.14.0",
                        "tables==3.6.1",
                        "tensorflow==1.14.0",
                        "terminado==0.8.3",
                        "testpath==0.4.4",
                        "tornado==6.0.3",
                        "traitlets==4.3.3",
                        "urllib3==1.25.8",
                        "wcwidth==0.1.8",
                        "webencodings==0.5.1",
                        "widgetsnbextension==3.5.1",
                        "xlrd==1.2.0",
                        "zipp==3.1.0"
                        ],
      zip_safe=False,
      entry_points={'console_scripts': ['chronix2grid=chronix2grid.main:generate_mp']}
)