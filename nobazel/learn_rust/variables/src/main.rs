// const THREE_HOURS_IN_SECONDS: u32 = 60 * 60 * 3;
// 
// fn main() {
// 
//     let guess: u32 = "42".parse().expect("Not a number!");
// 
//     let x = 5;
// 
//     let x = x + 1;
// 
//     {
//         let x = x * 2;
//         println!("The value of x in the inner scope is: {x}");
//     }
// 
//     println!("The value of x is: {x}");
// }

use std::io;

fn main() {
    let a = [1, 2, 3, 4, 5];

    println!("Please enter an array index.");

    let mut index = String::new();

    io::stdin()
        .read_line(&mut index)
        .expect("Failed to read line");

    let index: usize = index
        .trim()
        .parse()
        .expect("Index entered was not a number");

    let element = a[index];

    println!("The value of the element at index {index} is: {element}");

    let a = [10, 20, 30, 40, 50];
    let b = [10, 20, 30, 40, 50];

    let result = 'first: for element in a {
        println!("the value is: {element}");
        for j in b {
            println!("the value is: {j}");
            // 
            // break 'first 2;
        }
    };
    println!("Result: {result}");
}
