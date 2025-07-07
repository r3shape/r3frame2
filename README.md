![r3shape-labs](https://github.com/user-attachments/assets/ac634f13-e084-4387-aded-4679eb048cac)  
![PyPi Package version](https://img.shields.io/pypi/v/r3frame?style=for-the-badge&logo=pypi&logoColor=white&label=r3frame&labelColor=black&color=white&link=https%3A%2F%2Fpypi.org%2Fproject%2Fr3frame%2F2025.0.2%2F
)  
![GitHub Stars](https://img.shields.io/github/stars/r3shape/r3frame?style=for-the-badge&label=stars&labelColor=black&color=white)
![License](https://img.shields.io/badge/mit-badge?style=for-the-badge&logo=mit&logoColor=white&label=License&labelColor=black&color=white)
---  
#### **r3frame** is a collection of modules designed to bring structure to your next game project, without hindrance.

## Installation  
Install **r3frame** via pip:  

```sh
pip install r3frame2
```

## r3 Playground  
Once installed, you can run the **r3frame** playground demo by typing:  

```sh
r3 playground
```

This will launch an interactive example that is actively maintained and used to showcase **r3frame**'s capabilities.  

## Quick Start
Getting started is as simple as the following code:
```python
import r3frame2 as r3

class MyApp(r3.app.R3app):
    def __init__(self):
        super().__init__(title="MyApp")

    def init(self): pass
    def exit(self): pass

MyApp().run()
```

## Contributing  
Want to help improve **r3frame**? Feel free to contribute by submitting issues, suggesting features, or making pull requests!  

## License  
**r3frame** is open-source under the [**MIT License.**](LICENSE)
