
"""
Durga Puja Pandal Hopping Planner
Features:
- Object-Oriented Programming
- North and South Kolkata pandals
- Crowd-level queue estimation
- Nearest metro station information
- Estimated walking time
- Metro first/last train information
- Route time estimation
"""

from abc import ABC, abstractmethod
from enum import Enum


# --------------------------------------------------
# 1. CROWD LEVEL
# --------------------------------------------------

class CrowdLevel(Enum):
    LOW = 1.0
    MEDIUM = 1.8
    HIGH = 3.0


# --------------------------------------------------
# 2. METRO STATION
# --------------------------------------------------

class MetroStation:
    def __init__(
        self,
        name,
        line,
        first_train="Check official timetable",
        last_train="Check official timetable"
    ):
        self.name = name
        self.line = line
        self.first_train = first_train
        self.last_train = last_train

    def show_info(self):
        return (
            f"{self.name} | {self.line} | "
            f"First train: {self.first_train} | "
            f"Last train: {self.last_train}"
        )


# --------------------------------------------------
# 3. PANDAL
# --------------------------------------------------

class Pandal:
    BASE_VISIT_MIN = 30

    def __init__(
        self,
        name,
        area,
        base_queue_min=0,
        is_famous=False,
        nearest_metro=None,
        metro_walk_min=0
    ):
        self.name = name
        self.area = area
        self._base_queue_min = base_queue_min
        self.is_famous = is_famous
        self.nearest_metro = nearest_metro
        self.metro_walk_min = metro_walk_min

    def visit_time(self, crowd):
        queue = self._base_queue_min * crowd.value

        if self.is_famous:
            queue *= 1.5

        return round(self.BASE_VISIT_MIN + queue)


# --------------------------------------------------
# 4. ABSTRACT AREA
# --------------------------------------------------

class Area(ABC):
    def __init__(self, name):
        self.name = name
        self.pandals = []

    def add_pandal(
        self,
        name,
        base_queue_min=0,
        is_famous=False,
        nearest_metro=None,
        metro_walk_min=0
    ):
        pandal = Pandal(
            name,
            self,
            base_queue_min,
            is_famous,
            nearest_metro,
            metro_walk_min
        )
        self.pandals.append(pandal)
        return self

    @abstractmethod
    def travel_time(self):
        pass

    def __len__(self):
        return len(self.pandals)


# --------------------------------------------------
# 5. NORTH KOLKATA
# --------------------------------------------------

class NorthKolkata(Area):
    def __init__(self):
        super().__init__("North Kolkata")

        shobhabazar = MetroStation(
            "Shobhabazar Sutanuti",
            "Blue Line"
        )
        shyambazar = MetroStation(
            "Shyambazar",
            "Blue Line"
        )
        mg_road = MetroStation(
            "Mahatma Gandhi Road",
            "Blue Line"
        )

        self.add_pandal(
            "Kumartuli Park", 45, True,
            shobhabazar, 9
        ).add_pandal(
            "Baghbazar Sarbojanin", 30, True,
            shyambazar, 12
        ).add_pandal(
            "Shobhabazar Rajbari", 10, False,
            shobhabazar, 8
        ).add_pandal(
            "Hatibagan Sarbojanin", 15, False,
            shyambazar, 10
        ).add_pandal(
            "Ahiritola", 5
        ).add_pandal(
            "Kashi Bose Lane", 5,
            False, shyambazar, 12
        ).add_pandal(
            "Chaltabagan Lohapatti", 10,
            False, mg_road, 12
        ).add_pandal(
            "College Square", 15, True,
            mg_road, 8
        ).add_pandal(
            "Mohammad Ali Park", 30, True,
            mg_road, 10
        )

    def travel_time(self):
        return 20


# --------------------------------------------------
# 6. SOUTH KOLKATA
# --------------------------------------------------

class SouthKolkata(Area):
    def __init__(self):
        super().__init__("South Kolkata")

        kalighat = MetroStation(
            "Kalighat",
            "Blue Line"
        )
        rabindra_sarovar = MetroStation(
            "Rabindra Sarobar",
            "Blue Line"
        )
        netaji_bhavan = MetroStation(
            "Netaji Bhavan",
            "Blue Line"
        )
        jadavpur = MetroStation(
            "Kavi Nazrul",
            "Blue Line"
        )

        self.add_pandal(
            "Ballygunge Cultural", 20, True,
            kalighat, 15
        ).add_pandal(
            "Singhi Park", 25, True,
            kalighat, 12
        ).add_pandal(
            "Ekdalia Evergreen", 20, True,
            kalighat, 12
        ).add_pandal(
            "Suruchi Sangha", 30, True,
            netaji_bhavan, 20
        ).add_pandal(
            "Badamtala Ashar Sangha", 25, True,
            kalighat, 12
        ).add_pandal(
            "Mudiali", 15, False,
            rabindra_sarovar, 10
        ).add_pandal(
            "95 Pally", 20
        ).add_pandal(
            "Bakulbagan", 15
        ).add_pandal(
            "Tridhara", 15, False,
            kalighat, 15
        ).add_pandal(
            "Deshapriya Park", 30, True,
            kalighat, 12
        )

    def travel_time(self):
        return 25


# --------------------------------------------------
# 7. ROUTE
# --------------------------------------------------

class Route:
    CROSS_CITY_TRAVEL_MIN = 50

    def __init__(self, crowd=CrowdLevel.MEDIUM):
        self.stops = []
        self.crowd = crowd

    def add(self, pandal):
        self.stops.append(pandal)
        return self

    def total_minutes(self):
        total = 0

        for i, stop in enumerate(self.stops):
            total += stop.visit_time(self.crowd)

            if i > 0:
                previous = self.stops[i - 1]

                if previous.area is stop.area:
                    total += stop.area.travel_time()
                else:
                    total += self.CROSS_CITY_TRAVEL_MIN

        return total

    def report(self):
        print("\n" + "=" * 65)
        print("DURGA PUJA PANDAL HOPPING REPORT")
        print("Crowd level:", self.crowd.name)
        print("=" * 65)

        for i, stop in enumerate(self.stops, start=1):
            print(f"\n{i}. {stop.name}")
            print(f"   Area: {stop.area.name}")
            print(
                f"   Visit and queue time: "
                f"{stop.visit_time(self.crowd)} minutes"
            )

            if stop.nearest_metro is not None:
                print(
                    f"   Nearest metro: "
                    f"{stop.nearest_metro.name}"
                )
                print(
                    f"   Metro line: "
                    f"{stop.nearest_metro.line}"
                )
                print(
                    f"   Walking estimate: "
                    f"{stop.metro_walk_min} minutes"
                )
                print(
                    f"   Train information: "
                    f"{stop.nearest_metro.first_train} / "
                    f"{stop.nearest_metro.last_train}"
                )
            else:
                print("   Nearest metro: Not configured")

        total = self.total_minutes()

        print("\n" + "-" * 65)
        print(
            f"Estimated route duration: "
            f"{total // 60} hours {total % 60} minutes"
        )
        print(
            "Note: Metro walking estimates are displayed separately "
            "and are not added to the route total."
        )
        print(
            "Verify station distances and train timings before travel."
        )
        print("=" * 65)


# --------------------------------------------------
# 8. PLANNER
# --------------------------------------------------

class Planner:
    def __init__(self):
        self.north = NorthKolkata()
        self.south = SouthKolkata()

    def plan(self, area, count, crowd):
        route = Route(crowd)

        for pandal in area.pandals[:count]:
            route.add(pandal)

        return route

    def plan_both(self, per_area, crowd):
        route = Route(crowd)

        for pandal in self.north.pandals[:per_area]:
            route.add(pandal)

        for pandal in self.south.pandals[:per_area]:
            route.add(pandal)

        return route


# --------------------------------------------------
# 9. MAIN PROGRAM
# --------------------------------------------------

def main():
    planner = Planner()

    print("\nDURGA PUJA PANDAL HOPPING PLANNER")
    print("1. North Kolkata")
    print("2. South Kolkata")
    print("3. North and South Kolkata")

    try:
        choice = int(input("Choose your area (1-3): "))

        print("\nCrowd level")
        print("1. LOW - Lower estimated queue")
        print("2. MEDIUM - Moderate estimated queue")
        print("3. HIGH - Heavy estimated queue")

        crowd_choice = int(input("Choose crowd level (1-3): "))

        crowd_options = {
            1: CrowdLevel.LOW,
            2: CrowdLevel.MEDIUM,
            3: CrowdLevel.HIGH
        }

        if crowd_choice not in crowd_options:
            print("Invalid crowd choice.")
            return

        crowd = crowd_options[crowd_choice]

        if choice == 1:
            area = planner.north

        elif choice == 2:
            area = planner.south

        elif choice == 3:
            count = int(
                input("Number of pandals per area (1-9): ")
            )

            if not 1 <= count <= 9:
                print("Please enter a number from 1 to 9.")
                return

            planner.plan_both(count, crowd).report()
            return

        else:
            print("Invalid area choice.")
            return

        count = int(
            input(
                f"Number of pandals (1-{len(area)}): "
            )
        )

        if not 1 <= count <= len(area):
            print(
                f"Please enter a number from 1 to {len(area)}."
            )
            return

        planner.plan(area, count, crowd).report()

    except ValueError:
        print("Invalid input. Please enter a whole number.")


if __name__ == "__main__":
    main()
