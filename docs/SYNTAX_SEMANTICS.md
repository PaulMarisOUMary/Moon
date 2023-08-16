# Syntax and Semantics

## Introduction

### Overview

Introducing Moon, a new programming language designed with simplicity and accessibility at its core. Unlike many existing languages that can be complex and intimidating for beginners, Moon strips away unnecessary complexity and focuses on intuitive, minimalist syntax. By using familiar symbols and natural language constructs, it brings the power of coding to those who may have never thought it possible.

### Purpose and Design Goals

The primary purpose of this language is to make programming an enjoyable and comprehensible experience, especially for children and coding novices. The design goals are as follows:

1. Simplicity: Offer a gentle learning curve by using straightforward and minimalist syntax.
2. Intuitiveness: Create a language that resonates with natural language understanding, reducing the cognitive load for new learners.
3. Flexibility: Allow for growth and exploration by including essential programming concepts like variables, functions, loops, and conditions.
4. Engagement: Include features like human-readable explanations of code execution and potential gamification elements to keep learners engaged.

### Target Audience

Moon is aimed at children, educators, and anyone new to programming who wants to understand and experiment with coding in an unthreatening environment. Here's how different groups might use the language:

- Children: As a first introduction to programming, allowing them to create simple programs and understand foundational concepts.
- Educators: As a teaching tool in schools to introduce programming concepts in a more engaging and comprehensible way.
- Novice Programmers: For self-learners or those in coding bootcamps who need a gentle introduction to programming before moving on to more complex languages.
- Creative Exploration: For artists, writers, and other creatives who want to experiment with coding without getting bogged down in syntax.
- Advanced Programmers: As a tool for rapid prototyping and experimentation, allowing them to quickly test out ideas and concepts.

In essence, this language is more than just a programming language; it's a bridge to the world of computational thinking and a gateway to the vast possibilities of programming.

## Lexical Structure

### Comments

Comments are ignored by the compiler. There are two types of comments:

- Single-line comments start with `#` and end with a newline.
- Multi-line comments start with `(` and end with `)`.

Example:
```
# This is a single-line comment.

(
This is a multi
                -line comment.
)
```

### Identifiers

Identifiers are used to name variables, functions, classes, and other entities within the program. In our language, identifiers must adhere to the following rules:

- They must start with a letter or underscore (`_`).
- Can contain letters, numbers, and underscores.
- Are case-sensitive, so `name` and `Name` would be considered different identifiers.
- Cannot be one of the reserved [keywords](#keywords) of the language.
OR
- An identifier can be defined as a single emoji.

Example:

```
# Valid identifiers
apple
Apple
_apple
apple_pie
applePie
Apple123
🍎
🐋

# Invalid identifiers
1apple
1
_
100_000
10_
_10
🍎apple
apple🍎
w🐋e
```

### Literals

Literals are used to represent fixed values within the program. In our language, we support the following types of literals:
- Integer literals
- Floating-point literals
- String literals
- Boolean literals
- Null literals

#### Integer Literals

Integer literals are used to represent whole numbers.
Example:
```
42
-1
1000
```

#### Floating-Point Literals

Floating-point literals are used to represent decimal numbers.
Example:
```
3.14
-0.5
1.0
```

#### String Literals

String literals are used to represent text.
Example:
```
"Hello, World!"
"🍎 Apple"
```

#### Boolean Literals

Boolean literals are used to represent true and false values.
Example:
```
true
false
```

#### Null Literal

<!-- ! TODO "nothing" ? -->
Null literal is used to represent the absence of a value.
Example:
```
null
```

### Keywords

The following keywords are reserved and should not be used as identifiers:

The emoji ✅ means that the keyword is used in the language.
The emoji ❌ means that the keyword is not used for now in the language (but still reserved).

| Keyword   | Used |
|-----------|------|
| action    | ✅  |
| and       | ✅  |
| as        | ✅  |
| assert    | ❌  |
| async     | ❌  |
| await     | ❌  |
| continue  | ✅  |
| default   | ❌  |
| dict      | ✅  |
| elif      | ❌  |
| else      | ❌  |
| end       | ❌  |
| false     | ✅  |
| fail      | ✅  |
| from      | ✅  |
| for       | ❌  |
| global    | ❌  |
| has       | ✅  |
| if        | ✅  |
| in        | ❌  |
| is        | ✅  |
| isnt      | ✅  |
| lambda    | ❌  |
| list      | ✅  |
| null      | ✅  |
| not       | ✅  |
| nothing   | ❌  |
| or        | ✅  |
| pass      | ❌  |
| raise     | ✅  |
| result    | ✅  |
| test      | ✅  |
| thing     | ✅  |
| true      | ✅  |
| use       | ✅  |
| stop      | ✅  |
| while     | ✅  |
| yield     | ❌  |

## Syntax

### Data Types

#### Primitive Types

- Integer: `count is 5`
- Floating-point: `pi is 3.14`
- String: `name is "Alice"`
- Boolean: `fact is true` or `lie is false`
- Null: `empty is null`

#### Composite Types

- Lists: Ordered collections of elements represented as:
```
mylist is list
    1
    "Alex"
```

- Dictionaries: Key-Value paired collections represented as:
```
mydict is dict
    "name" is "Alex"
    -85 is 85
```

### Variables

Variables are used to store values within the program. In our language, variables must adhere to the identifiers rules.

#### Declaration and Initialization

Variables are declared and then initialized using the `is` keyword.
Example:
```
count is 5
pi is 3.14
name is "Alice"
fact is true
empty is null
```

#### Scope

Here are the different types of scopes:
- Local Scope: A variable defined inside a function is said to have a local scope. It can only be accessed within that function, not outside it.
- Enclosing Scope: This is a special scope that exists when you have a function inside another function (nested functions). An inner function has access to the variables of the outer function that contains it.
- Global Scope: A variable that is defined outside any function has a global scope. This means it can be accessed from anywhere in the code, both inside and outside functions.
- Built-in Scope: This scope refers to the names in the pre-defined built-ins module that this language provides.

### Expressions

Expressions are used to represent computations within the program. In our language, we support the following types of expressions:
- Arithmetic expressions
- Logical expressions
- Relational expressions

#### Arithmetic Expressions

The following arithmetic operators are supported:

| Operator | Description    | Example        |
|----------|----------------|----------------|
| `+`      | Addition       | `1 + 2`        |
| `-`      | Subtraction    | `1 - 2`        |
| `*`      | Multiplication | `1 * 2`        |
| `/`      | Division       | `1 / 2`        |
| `%`      | Modulo         | `1 % 2`        |
| `**`     | Exponentiation | `1 ** 2`       |

#### Logical Expressions

The following logical operators are supported:

| Operator | Description | Example          |
|----------|-------------|------------------|
| `and`    | Logical And | `true and false` |
| `or`     | Logical Or  | `true or false`  |
| `not`    | Logical Not | `not true`       | 
<!-- ! TODO -->

#### Relational Expressions

The following comparison operators are supported:

| Operator | Description           | Example               |
|----------|-----------------------|-----------------------|
| `<`      | Less Than             | `1 < 2`               |
| `<=`     | Less Than or Equal    | `1 <= 2`              |
| `>`      | Greater Than          | `1 > 2`               |
| `>=`     | Greater Than or Equal | `1 >= 2`              |
| `is`     | Equal                 | `1 is 1`              |
| `isnt`   | Not Equal             | `1 isnt 2`            |

### Control Structures

#### Conditional Statements

Conditional statements are used to execute different blocks of code based on a condition. In our language, we support the following types of conditional statements:
- If statements (`if`)
- Else statements (`else`)

##### If Statements

If statements are used to execute a block of code if a condition is true.
Example:
```
if 1 < 2
    print "1 is less than 2"
```

##### Else Statements

Else statements are used to execute a block of code if the initial condition is false.
Example:
```
if 1 > 2
    print "1 is greater than 2"
else
    print "1 is not greater than 2"
```

#### Looping Structure

Looping structures are used to execute a block of code repeatedly. In our language, we support the following types of looping structures:
- While loops (`while`)

The following looping keywords are supported:
- `continue`: Used to skip the current iteration of the loop and move on to the next one.
- `stop`: Used to exit the loop from executing any further.

Example:
```
count is 0
while count < 10
    print count
    count is count + 1
```

#### Try-Catch and Raise Statements

Try-catch statements are used to handle errors in the code. In our language, try-catch statements are named `test` and `fail`.

Use the `test` keyword to define a block of code that may throw an error. Use the `fail` keyword to define a block of code that will be executed if an error is thrown.
The `error` keyword is used to throw manualy an error.

Example:
```
test
    error "Something went wrong"
fail
    print "An error occurred"
```

### Functions

Functions are used to group a set of statements together and execute them on call. In our language, functions must adhere to the following rules:
- They must start with the `action` keyword.
- They must be followed by an identifier, (name of the function).
- They can be followed by a set of parameters named as an identifier.

Return values are optional. If a function does not return a value, it is said to return `null`.
The `result` keyword is used to return a value from a function.

To call a function, you just need to use its name followed by the arguments if any.

Example:
```
action addNumbers a b
    result a + b

sum is addNumbers 1 2
print sum
# Output: 3
```

### Classes

#### Declaration and Initialization

Define a class using the `thing` keyword followed by an identifier (name of the class).
<!-- ! TODO empty class -->
Example:
```
thing Human
```

#### Properties

Properties are used to store values within a class. In our language, properties must adhere to the following rules:
- They must start with the `has` keyword.
- They must be followed by an identifier, (name of the property).

Example:
```
thing Human
    has name
    has age
```

#### Methods

Methods are used to define the behavior of a class. In our language, methods must adhere to the function rules.

Example:
```
thing Human
    has name
    has age

    action saySomething message
        print "Hello, " + message

myHuman is Human
myHuman saySomething "World!"
# Output: Hello, World!
```

#### Constructors

Constructors are used to initialize the properties of a class. In our language, constructors is a special method named `default`.

If you pass the same parameters as the properties of the class, the values passed to the constructor method paramaters will be shared automaticly to the properties of the class.
Example:
```
thing Robot
    has name
    has batteryLevel
    has serialNumber

    action default name batteryLevel
        serialNumber is 1 + name

myRobot is Robot "Alex" 85

print myRobot name
# Output: Alex
print myRobot batteryLevel
# Output: 85
print myRobot serialNumber
# Output: 1Alex
```

#### Inheritance

Inheritance is used to define a relationship between two classes. In our language, inheritance is defined using the `is` keyword.

Example:
```
thing Animal
    has name

    action default name
        (
            no implementation needed because the attribute 'age'
            is shared with the member 'age' of the class
            this is happening because they share the same name,
            and so the value passed to the class constructor is
            automatically assigned to the member 'age'
        )

thing Dog
    is Animal
    has age

    (override the constructor of the class 'Animal')
    action default name age
        ( no implementation needed )

    action bark
        print "Woof!"
```

### Modules

#### Module Definition

Each file is a module. The name of the module is the name of the file.

Example:

```
# file: hello.moon
action say
    print "Hello, World!"
```

#### Module Import

This is how we import a module, using the keyword `from` followed by the path of the module.
Right now narrowing the import to a specific function is not supported and the only valid narrowing is `*` which basically means import everything within this module.
Example:

```
from "path/to/module.moon" use *
```

To use advanced standard library modules, you can use the keyword `use` followed by the name of the module.
Example:
```
use module
```
More about the standard library [here](#standard-library).

### Tabulations

Tabulations are used to group a set of statements together. In our language, tabulations can be either a set of spaces or a tabulation character.

One tabulation is equal to either 4 spaces or 1 tabulation character.
| Valid tabulation unicode | Description  |
|--------------------------|--------------|
| `U+0020`                 | 4 spaces     |
| `U+0009`                 | 1 tabulation |

### Separator

#### Statements Separator

In our language, we separate statements using a newline.

#### Token Separator

A token is the smallest element of a program that is meaningful to the compiler or interpreter.

- It's a sequence of characters that represents a single unit of meaning or syntax.
- Tokens can include identifiers (e.g., variable names), literals (e.g., numbers, strings), operators (e.g., +, -, *), keywords (e.g., if, while), and various symbols.

In our language, we separate tokens using a space (only if the token is followed by another token).

## Semantics

### Execution Model

The execution model of the language is based on the following steps:
<!-- ! TODO -->

### Type System

The type system in our language is designed with simplicity and intuition in mind. Here's how it functions:
- Type Checking: The language automatically identifies the data type of the value assigned to a variable. Types include integers, floats, strings, booleans, etc.
- Type Inference: The language automatically infers the data type of the value returned by a function. This means you don't have to specify the return type of a function.
- Type Coercion: The language automatically converts values from one type to another when necessary. For example, if you try to add an integer and a float, the integer will be converted to a float before the addition is performed.
-Type Casting: Automatic type casting is not supported. Specific functions or commands will be provided for manual casting if required.
- Type Declaration: Type declaration is implicit. The type is determined by the value assigned to the variable.

### Variable Lifetime and Scope

Understanding the lifetime and scope of variables is key to managing data within the code.

- Global Variables: These are accessible throughout the entire program. They are defined outside of any actions or things and can be used anywhere.
- Local Variables: These are defined within actions or things and only accessible within those specific areas.
- Lifetime Management: Local variables have lifetimes tied to the actions or things they're defined in. Once the action or thing ends, the variable is destroyed. Global variables last for the entire execution of the program.

### Error Handling

The error handling in our language is designed to be transparent and informative.

- Error Messages: Errors in the code (such as type mismatches or undefined variables) will result in clear and human-readable error messages.
- Exception Throwing: Specific exceptions for various errors will not be thrown. Instead, a general error message will be shown, and the program will stop execution.
- Error Recovery: At the current stage, error recovery is not implemented. Errors must be fixed by the programmer.

### Concurrency

Concurrency is not supported in our language. This means that only one action can be executed at a time.

## Standard Library

### Built-in Functions

The following built-in functions are provided by the language:

| Function | Description |
|----------|-------------|
| `print`  | Prints the given value to the console. |
| `ask  `  | Asks the user for input and returns the value. |
| `random` | Returns a random number between 0 and 1. |
| `time`   | Returns the current time in milliseconds. |
| `sleep`  | Pauses the execution of the program for the given number of milliseconds. |

### Built-in Modules

The following built-in modules are provided by the language:
- `list`: Provides list manipulation functions like `size`, `get`, `set`, etc.
- `dict`: Provides dictionary manipulation functions like `size`, `keys`, `values`, etc.
- `string`: Provides string manipulation functions like `length`, `replace`, `split`, etc.
- `math`: Provides mathematical functions like `sin`, `cos`, `tan`, `sqrt`, etc.
- `file`: Provides file manipulation functions like `read`, `write`, `append`, etc.
- `draw`: Provides drawing functions like `circle`, `rectangle`, `line`, etc.

### Standard Modules

In the current stage, there is no standard modules.

## Examples

<!-- ! TODO -->

## References

<!-- ! TODO -->