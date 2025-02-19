// main.rs
//$env:PATH += ";C:\msys64\mingw64\bin"

#![no_std] //no liking to rust std lib
#![no_main]//disable entry point

use core::panic::PanicInfo;

//call on panic, no return, loop forever
#[panic_handler]
fn panic(_info: &PanicInfo) -> ! {
    loop {}
}

#[no_mangle]//don't mangle func name
pub extern "C" fn _start() -> ! {
    vga_buffer::print_something();
    loop{}
}

mod vga_buffer;
