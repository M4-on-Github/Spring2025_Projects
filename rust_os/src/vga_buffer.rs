#[allow(dead_code)]
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
#[repr(u8)]
pub enum Color {
    Black = 0,
    Blue = 1,
    Green = 2,
    Cyan = 3,
    Red = 4,
    Magenta = 5,
    Brown = 6,
    LightGray = 7,
    DarkGray = 8,
    LightBlue = 9,
    LightGreen = 10,
    LightCyan = 11,
    LightRed = 12,
    Pink = 13,
    Yellow = 14,
    White = 15,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
#[repr(transparent)]
struct ColorCode(u8);

impl ColorCode {
    /// Create a new `ColorCode` with the given foreground and background colors.
    fn new(foreground: Color, background: Color) -> ColorCode {
        ColorCode((background as u8) << 4 | (foreground as u8))
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
#[repr(C)]
struct screenChar {
    ascii_character: u8,
    color_code: ColorCode,
}

const Buffer_Height: usize = 25;
const Buffer_Width: usize = 80;

#[repr(transparent)]
struct Buffer {
    chars:[[screenChar; Buffer_Width]; Buffer_Height],
}

//actually write to the screen
pub struct Writer {
    column_position: usize,
    color_code: ColorCode,
    buffer: &'static mut Buffer,
}

//modify the buffer's characters (read through, shld be intuitive lol
impl Writer {
    pub fn write_byte(&mut self, byte: u8) {
        match byte {
            b'\n' => self.new_line(),
            byte => {
                if self.column_position >= Buffer_Width {
                    self.new_line();
                }
            let row = Buffer_Height - 1;
            let col = self.column_position;

            let color_code = self.color_code;
            self.buffer.chars[row][col] = screenChar {
                ascii_character: byte,
                color_code,
            };
            self.column_position += 1;
            }
        }
    }
    fn new_line(&mut self) {/* To be implemented! */}
}

//convert to bytes and write to screen
impl Writer {
    pub fn write_string(&mut self, s: &str) {
        for byte in s.bytes() {
            match byte{
                0x20..=0x7e | b'\n' => self.write_byte(byte),
                _=> self.write_byte(0xfe), //not printable cases
            }
        }
    }
}

pub fn print_something() {
    let mut writer = Writer {
        column_position: 0,
        color_code: ColorCode::new(Color::Yellow, Color::Black),
        buffer: unsafe { &mut *(0xb8000 as *mut Buffer) },
    };

    writer.write_byte(b'H');
    writer.write_string("ello ");
    writer.write_string("Wörld!");
}

