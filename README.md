// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract TriangleChecker {
    function checkTriangle(uint a, uint b, uint c) public pure returns (string memory triangleType, uint areaTimes100) {
        // Check if valid triangle (Triangle Inequality Theorem)
        if (a + b > c && a + c > b && b + c > a) {
            // Determine the type of triangle
            if (a == b && b == c) {
                triangleType = "Equilateral";
            } else if (a == b || b == c || a == c) {
                triangleType = "Isosceles";
            } else if (a * a + b * b == c * c || a * a + c * c == b * b || b * b + c * c == a * a) {
                triangleType = "Right Angled";
            } else {
                triangleType = "Scalene";
            }

            // Calculate semi-perimeter (s)
            uint s = (a + b + c) / 2;

            // Heron's formula for area: sqrt(s * (s - a) * (s - b) * (s - c))
            uint temp = s * (s - a) * (s - b) * (s - c);
            areaTimes100 = sqrt(temp) * 100;
        } else {
            triangleType = "Not a triangle";
            areaTimes100 = 0;
        }
    }

    // Function to calculate square root using the Babylonian method
    function sqrt(uint x) internal pure returns (uint y) {
        uint z = (x + 1) / 2;
        y = x;
        while (z < y) {
            y = z;
            z = (x / z + z) / 2;
        }
    }
}# RootSense