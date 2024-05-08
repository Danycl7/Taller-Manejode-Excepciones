class Frame:
    def __init__(self):
        self.rolls = []
        self.complete = False

    def add_roll(self, pins):
        if len(self.rolls) < 2 or (len(self.rolls) == 2 and self.is_tenth_frame() and self.is_spare_or_strike()):
            self.rolls.append(pins)
            if len(self.rolls) == 2 and not self.is_tenth_frame():
                self.complete = True
            if self.is_tenth_frame() and (len(self.rolls) == 3 or (len(self.rolls) == 2 and not self.is_spare_or_strike())):
                self.complete = True
        else:
            raise ValueError("No more rolls can be added to this frame.")

    def is_strike(self):
        return self.rolls[0] == 10

    def is_spare(self):
        return len(self.rolls) > 1 and sum(self.rolls[:2]) == 10

    def is_spare_or_strike(self):
        return self.is_strike() or self.is_spare()

    def is_tenth_frame(self):
        return False

    def score(self):
        return sum(self.rolls)

class TenthFrame(Frame):
    def __init__(self):
        pass
    
    def add_roll_tenth_frame(self, pins):
        if len(self.rolls) < 3:
            self.rolls.append(pins)
            if len(self.rolls) == 1 and not self.is_strike():
                self.complete = False  
            elif len(self.rolls) == 2 and self.is_strike():
                self.complete = False  
            elif len(self.rolls) == 2 and not self.is_strike() and not self.is_spare():
                self.complete = True   
            elif len(self.rolls) == 2 and self.is_spare():
                self.complete = False  
            elif len(self.rolls) == 3:
                self.complete = True   
        else:
            raise ValueError("No more rolls can be added to this frame.")

    def is_tenth_frame(self):
        return True

class BowlingGame:
    def __init__(self):
        self.frames = [Frame() for _ in range(9)] + [TenthFrame()]
        self.current_frame = 0

    def roll(self, pins):
        if self.current_frame >= 10:
            raise Exception("All frames are already played.")
        
        frame = self.frames[self.current_frame]
        frame.add_roll(pins)
        
        if frame.complete:
            self.current_frame += 1

    def score(self):
        total_score = 0
        for i in range(10):
            frame = self.frames[i]
            if frame.is_strike():
                total_score += 10 + self.strike_bonus(i)
            elif frame.is_spare():
                total_score += 10 + self.spare_bonus(i)
            else:
                total_score += frame.score()
        return total_score

    def strike_bonus(self, index):
        bonus = 0
        if index + 1 < len(self.frames):
            next_frame = self.frames[index + 1]
            if len(next_frame.rolls) > 0:
                bonus += next_frame.rolls[0]
            if len(next_frame.rolls) > 1:
                bonus += next_frame.rolls[1]
            elif index + 2 < len(self.frames):
                bonus += self.frames[index + 2].rolls[0]
        return bonus

    def spare_bonus(self, index):
        if index + 1 < len(self.frames) and len(self.frames[index + 1].rolls) > 0:
            return self.frames[index + 1].rolls[0]
        return 0

    def is_game_over(self):
        return self.current_frame == 10

def main():
    game = BowlingGame()
    while not game.is_game_over():
        current_frame = game.frames[game.current_frame]
        try:
            print(f"Frame {game.current_frame + 1}, Roll {len(current_frame.rolls) + 1}")
            pins = int(input("Enter pins knocked down: "))

            
            if pins < 0 or pins > 20:
                print("Invalid input! Please enter a number from 0 to 20.")
                continue

           
            if not current_frame.is_tenth_frame() and len(current_frame.rolls) == 1:
                remaining_pins = 20 - current_frame.rolls[0]
                if pins > remaining_pins:
                    print(f"Invalid input! Only {remaining_pins} pins are left.")
                    continue

            
            if current_frame.is_tenth_frame():
                if len(current_frame.rolls) == 1 and not current_frame.is_strike():
                    remaining_pins = 20 - current_frame.rolls[0]
                    if pins > remaining_pins:
                        print(f"Invalid input! Only {remaining_pins} pins are left.")
                        continue
                elif len(current_frame.rolls) == 2 and current_frame.is_strike() and current_frame.rolls[1] < 20:
                    remaining_pins = 20 - current_frame.rolls[1]
                    if pins > remaining_pins:
                        print(f"Invalid input! Only {remaining_pins} pins are left.")
                        continue

            game.roll(pins)
        except ValueError:
            print("Please enter a valid integer number.")
        except Exception as e:
            print(str(e))

    print("Game over! Your final score is:", game.score())

if __name__ == "__main__":
    main()
