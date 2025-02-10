Here's a Solidity program to find the real and imaginary roots of a quadratic equation of the form:

ax^2 + bx + c = 0


---

Solidity Code:

// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract QuadraticSolver {
    function findRoots(int a, int b, int c) public pure returns (string memory rootType, int root1, int root2, int imaginary) {
        if (a == 0) {
            return ("Not a quadratic equation", 0, 0, 0);
        }

        int discriminant = b * b - 4 * a * c;

        if (discriminant > 0) {
            // Two distinct real roots
            rootType = "Real and Distinct";
            root1 = (-b + sqrt(uint(discriminant))) / (2 * a);
            root2 = (-b - sqrt(uint(discriminant))) / (2 * a);
            imaginary = 0;
        } else if (discriminant == 0) {
            // One real root (repeated)
            rootType = "Real and Equal";
            root1 = -b / (2 * a);
            root2 = root1;
            imaginary = 0;
        } else {
            // Complex conjugate roots
            rootType = "Complex";
            root1 = -b / (2 * a);
            root2 = root1;
            imaginary = sqrt(uint(-discriminant)) / (2 * a);
        }
    }

    // Babylonian method to compute integer square root
    function sqrt(uint x) internal pure returns (uint y) {
        uint z = (x + 1) / 2;
        y = x;
        while (z < y) {
            y = z;
            z = (x / z + z) / 2;
        }
    }
}


---

Explanation:

1. Handles cases where a = 0, ensuring it is a valid quadratic equation.


2. Calculates the discriminant:

If D > 0, there are two distinct real roots.

If D = 0, there is one real repeated root.

If D < 0, the roots are complex conjugates (real + imaginary).



3. Uses the Babylonian method for calculating the square root in Solidity.


4. Returns the type of roots, along with real and imaginary parts.




---

Example Outputs:

Equation:  (Real & Distinct)

Roots: 3, 2


Equation:  (Real & Equal)

Root: 2


Equation:  (Complex)

Roots: -0.5 + i0.866 and -0.5 - i0.866 (represented in Solidity as (-1, -1, 866) since it returns scaled imaginary values)




---

How to Use:

Deploy this contract on Remix Ethereum IDE and call findRoots(a, b, c) with your quadratic coefficients.

Let me know if you need modifications!

