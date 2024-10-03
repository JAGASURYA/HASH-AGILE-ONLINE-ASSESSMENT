package main

import (
	"fmt"
	"math"
)

func main() {
	arr := []int{10, 10, 10}
	secondLargest := findSecondLargest(arr)
	if secondLargest != -1 {
		fmt.Printf("The second largest element is: %d\n", secondLargest)
	} else {
		fmt.Println("There is no second largest element.")
	}
}
func findSecondLargest(arr []int) int {
	if len(arr) < 2 {
		return -1 // Not enough elements to find second largest
	}
	largest := math.MinInt32
	secondLargest := math.MinInt32
	for _, num := range arr {
		if num > largest {
			secondLargest = largest
			largest = num
		} else if num > secondLargest && num < largest {
			secondLargest = num
		}
	}
	// If secondLargest is still the minimum value, return -1
	if secondLargest == math.MinInt32 {
		return -1
	}
	return secondLargest
}
