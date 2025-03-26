import os
import time
import itertools
from django.core.management.base import BaseCommand
from rich import print

class Command(BaseCommand):
    help = "Displays a ship animation for logistics branding"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("\n🚀 Welcome to [bold cyan]Logistics CLI[/bold cyan]!"))

        ship_frames = [
            """
                         |
                         |    |  |      
                    )_)  )_)  )_)  )_)  
                   )___))___))___))___) 
                 )____)____)____)_____) 
             ____|____|____|____|____|____
        ----\\                   /---------
            """,
            """
                          |
                          |    |  |      
                     )_)  )_)  )_)  )_)  
                    )___))___))___))___) 
                  )____)____)____)_____) 
              ____|____|____|____|____|____
         ----\\                   /---------
            """,
        ]

        wave_patterns = itertools.cycle([
            " ~~~~ ~~~~ ~~~~ ~~~~ ~~~~ ",
            "  ~~~~ ~~~~ ~~~~ ~~~~ ~~~~",
            "   ~~~~ ~~~~ ~~~~ ~~~~ ~~~",
            "    ~~~~ ~~~~ ~~~~ ~~~~ ~~",
            "   ~~~~ ~~~~ ~~~~ ~~~~ ~~~",
            "  ~~~~ ~~~~ ~~~~ ~~~~ ~~~~",
            " ~~~~ ~~~~ ~~~~ ~~~~ ~~~~ ",
        ])

        for _ in range(20):
            for frame in ship_frames:
                os.system("cls" if os.name == "nt" else "clear")
                waves = next(wave_patterns)
                print(f"[bold cyan]{frame}[/bold cyan]")
                print(f"[bold blue]{waves}[/bold blue]")
                time.sleep(0.2)
