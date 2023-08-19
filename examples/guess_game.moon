(
	Guess the number
    This is a simple example made to show
    the use of: while loop, if, skip and
    stop statements.
)

to_guess is 14

while true
	guess is ask "Type your guess: "

	if guess < to_guess
		print "Its More"

	if guess > to_guess
		print "Its Less"

	if guess isnt to_guess
		skip

	stop

print "Congrats you won !"