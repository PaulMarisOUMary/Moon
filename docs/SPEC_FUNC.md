# Functional Specification

v 1.0

## Context

### Introduction

This Functional Specification provides a detailed look of this programming language project, focusing on its design, features, and core concepts.
The goal is to offer an accessible, intuitive and easy language tailored for both beginners and experienced developers.

### Purpose

The primary purpose of this language is to simplify the learning curve for new programmers while providing a robust set of features for more advanced users.

Throughout this project, we will focus on the following:
1. Learning Curve: The language should be easy to learn and use.
    a. How can we make it easier for children to learn programming ?
    b. How can language evolve with children as they learn new concept ?
2. Easy accessiblity: The language should be accessible to a wide range of users.
    a. How to ensure that language is accessible to different age and skill levels ?
    b. How to make it easier for children to learn programming ?
3. Make programming interesting: The language should be fun to use.
    a. How to make programming fun ?
4. Useful programming: The language should be useful for a wide range of tasks.
5. Safe programming: The language should be safe to use.

### Scope

The current version of the language encompasses basic constructs such as variable handling, control flow, error handling, and a standard library. Future iterations may include concurrency support and extended library functionalities.

## Functional Requirements

### Semantics

- Execution Model: Sequential execution; no concurrency support.
- Type System: Inclusive of type checking, inference, coercion, casting, and declaration.
- Variable Lifetime & Scope: Differentiating between global and local variables.
- Error Handling: User-friendly error messages and error handling.

### Standard Library

- Built-in Functions: A set of basic functions such as print, ask, etc.
- Built-in Modules: Various modules for handling lists, strings, math, files, and drawings.

### User Interaction

- Interactive Console: Real-time coding and testing.
- Integrated Development Environment (IDE): Syntax highlighting, code completion, and other features.

## Acceptance Criteria

- User-Friendly Syntax: Intuitive for newcomers.
- Robust Error Handling: Clear and informative error messages.
- Comprehensive Standard Library: Useful for a wide range of tasks.

## Design

### Language Design

The language is designed to be simple and intuitive, with a focus on readability and ease of use. The syntax is designed to be consistent and predictable, with a minimal number of keywords and operators.

### IDE Details

Real-time syntax checking and highlighting.
Integration with the standard library for immediate access to built-in functions and modules.
Capability to execute code snippets and view immediate output.

### Accessiblity

Accessibility is vital in ensuring that the language is usable by a diverse range of individuals, including children and those with different skill levels. Accessibility considerations include:

- Providing a friendly and intuitive language syntax.
- Offering, guides.
- Adapting the language's complexity and vocabulary to suit the intended audience, with potential for growth as the user gains more experience.

## Non-functional Requirements

- Reliability: Stable performance and absence of critical bugs.
- Accessibility: Designed with an array of users in mind, including those new to programming.
- Acceptable Performance: Reasonable execution time and resource utilization.
- Testing strategy: Unit testing, integration testing, and user testing.

## Out of Scope

- High Efficiency: Efficient execution and resource utilization.
- Concurrency: Not supported in the current version.
- Asynchronous Programming: Not supported in the current version.
- Advanced Error Recovery: Errors must be fixed by the programmer.

## Testing Strategy

- Unit Testing: Testing of individual functions and modules.
- Integration Testing: Testing of the language as a whole.

## Security

The design of the programming language should take into account the unique security needs of children. This includes:

- Ensuring privacy by not collecting or storing personal information without proper consent.
- Providing clear guidelines and warnings about potential risks, especially if internet access or file system access is part of the functionality.

## Glossary

- Concurrency: Parallel execution of tasks.
- Asynchronous Programming: Non-blocking execution of tasks and events.
- Type Inference: Automatic determination of data types.
- Global/Local Variables: Scope of variable access.
- IDE: Integrated Development Environment.
- Children: Users of the language, aged from 10 to infinity.

## Conclusion

This Functional Specification outlines the structure, functionality, design, and non-functional requirements of the programming language. It serves as a guide for the development of the language and its core concepts.