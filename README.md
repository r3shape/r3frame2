![r3shape-labs](https://github.com/user-attachments/assets/ac634f13-e084-4387-aded-4679eb048cac)  
![PyPi Package version](https://img.shields.io/pypi/v/r3frame?style=for-the-badge&logo=pypi&logoColor=white&label=r3frame&labelColor=black&color=white&link=https%3A%2F%2Fpypi.org%2Fproject%2Fr3frame%2F2025.0.2%2F
)  
![GitHub Stars](https://img.shields.io/github/stars/r3shape/r3frame?style=for-the-badge&label=stars&labelColor=black&color=white)
![License](https://img.shields.io/badge/mit-badge?style=for-the-badge&logo=mit&logoColor=white&label=License&labelColor=black&color=white)
---  
#### **r3frame2** is a collection of modules, classes and utilities designed to bring structure to your next project, without hindrance. Providing a robust and extensible development framework for many kinds of multimedia applications.

## Installation  
Install **r3frame** via pip:  

```sh
pip install r3frame2
```

## r3 Playground  
Once installed, you can run the playground demo by typing:  

```sh
r3playground
```

This will launch an interactive example that is actively maintained and used to showcase **r3frame**'s capabilities.  

## Quick Start
Getting started is as simple as the following code:
```python
import r3frame2 as r3

class MyScene(r3.app.R3scene):
    def __init__(self, app):
        super().__init__(app)

    def init(self):
        # load an R3entity
        self.database.load_entity("player", [100, 100])
        
        # query said entity and toggle physics on it
        self.player = self.database.query_entity("player")
        self.physics.toggle_transform(self.player)
    
    def exit(self): pass

    def events(self):
        # handle movement along the x-axis
        if self.app.events.key_held(self.app.keyboard.A):
            self.physics.set_velocity(self.player, dx=-100)
        if self.app.events.key_held(self.app.keyboard.D):
            self.physics.set_velocity(self.player, dx=100)

        # handle movement along the y-axis
        if self.app.events.key_held(self.app.keyboard.W):
            self.physics.set_velocity(self.player, dy=-100)
        if self.app.events.key_held(self.app.keyboard.S):
            self.physics.set_velocity(self.player, dy=100)

    def update(self, dt: float): pass

    def render(self):
        # queue a render call for our player (0x0000 = Opaque Render Phase)
        self.renderer.queue(r3.resource.R3renderCall(0x0000, self.player.pos, self.player.surface))

class MyApp(r3.app.R3app):
    def __init__(self):
        super().__init__(title="MyApp")

    def init(self):
        self.add_scene("player", MyScene)
        self.set_scene("player")

    def exit(self): pass

MyApp().run()
```

## Contributing  
Want to help improve **r3frame**? Feel free to contribute by submitting issues, suggesting features, or making pull requests!  

## License  
**r3frame** is open-source under the [**MIT License.**](LICENSE)
