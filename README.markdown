# Abandoned! #

GarlicSim used to be an ambitious open-source project, but after 2.5 years of work and little public interest it was abandoned. It's no longer being actively developed.

The full story: (http://blog.ram.rachum.com/post/24682447796/garlicsim-is-dead-long-live-python-toolbox)

# Documentation #

[Main documentation site](http://docs.garlicsim.org)

[Installation](http://docs.garlicsim.org/intro/installation/developers/python-2.x.html)

[FAQ](http://docs.garlicsim.org/misc/faq.html)

[Mailing lists](http://docs.garlicsim.org/misc/mailing-lists.html)

If you wish, it's possible to just run the GUI and play with it without installing anything. To do so, download the repo and run the `run_gui.py` file in the root folder.


# What is GarlicSim? #

GarlicSim is an ambitious open-source project in the field of scientific computing, specifically computer simulations. It attempts to redefine the way that people think about computer simulations, making a new standard for how simulations are created and used.

GarlicSim is a platform for writing, running and analyzing simulations. It is general enough to handle any kind of simulation: Physics, game theory, epidemic spread, electronics, etc.

When you're writing a simulation, about 90% of the code you write is boilerplate; code that isn't directly related to the phenomenon you're simulating, but is necessary for your simulation to work. The aim of GarlicSim is to write that 90% of the code once and for all, and to do it well, so you could concentrate on the important 10%.

GarlicSim defines a new format for simulations. It's called a **simulation package**, and often abbreviated as **simpack**. For example, say you are interested in simulating the interaction of hurricane storms. It is up to you to write a simpack for this type of simulation. The simpack is simply a Python package which defines a few special functions according to the GarlicSim simpack API, the most important function being the **step function**.

The beauty is that since so many simulation types can fit into this mold of a simpack, the tools that GarlicSim provides can be used across all of these different domains. Once you plug your own simpack into GarlicSim, you're ready to roll. All the tools that GarlicSim provides will work with your simulation.

Additionally, GarlicSim will eventually be shipped with a standard library of simpacks for common simulations, that the user may find useful to use as-is, or with his own modifications.

For a more thorough introduction to how GarlicSim works, check out the [documentation](http://docs.garlicsim.org).

GarlicSim itself is written in pure Python. The speed of simulations is mostly dependent on the simpack's performance - So it is possible to use C code in a simpack to make things faster.


# Mailing lists #

All general discussion happens at **[the GarlicSim Google Group](https://groups.google.com/forum/#!forum/garlicsim)**. If you need help with GarlicSim, you're welcome to post your question and we'll try to help you.

The development mailing list is **[GarlicSim-dev](https://groups.google.com/forum/#!forum/garlicsim-dev)**. This is where we discuss the development of GarlicSim itself.


# Core and GUI #

This repository contains three packages: `garlicsim`, which is the core logic, `garlicsim_lib`, which is a collection of simpacks, and `garlicsim_wx`, which is the wxPython-based GUI.

They are all distributed under the **LGPL2.1 license**. 


# Python versions #
 
GarlicSim supports Python versions 2.5 and up, not including Python 3.x.

There is a [separate fork of GarlicSim](http://github.com/cool-RR/GarlicSim-for-Python-3.x) that supports Python 3.x. Take note though that it does not contain a GUI, because wxPython does not support Python 3.x.

GarlicSim was created by Ram Rachum. I also provide [freelance Django/Python development services](https://chipmunkdev.com).
