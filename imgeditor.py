"""
The primary controller module for the Imager application

This module provides all of the image processing operations that are called whenever you 
press a button. Some of these are provided for you and others you are expected to write
on your own.

Based on an original file by Dexter Kozen (dck10) and Walker White (wmw2)

Author: Walker M. White (wmw2)
Date:    October 20, 2017 (Python 3 Version)
"""
import imghistory
import math


class Editor(imghistory.ImageHistory):
    """
    A class that contains a collection of image processing methods
    
    This class is a subclass of ImageHistory.  That means it inherits all of the methods
    and attributes of that class.  We do that (1) to put all of the image processing
    methods in one easy-to-read place and (2) because we might want to change how we 
    implement the undo functionality later.
    
    This class is broken up into three parts (1) implemented non-hidden methods, (2)
    non-implemented non-hidden methods and (3) hidden methods.  The non-hidden methods
    each correspond to a button press in the main application.  The hidden methods are
    all helper functions.
    
    Each one of the non-hidden functions should edit the most recent image in the
    edit history (which is inherited from ImageHistory).
    """
    
    # PROVIDED ACTIONS (STUDY THESE)
    def invert(self):
        """
        Inverts the current image, replacing each element with its color complement
        """
        current = self.getCurrent()
        for pos in range(current.getLength()):
            rgb = current.getFlatPixel(pos)
            red   = 255 - rgb[0]
            green = 255 - rgb[1]
            blue  = 255 - rgb[2]
            rgb = (red,green,blue) # New pixel value
            current.setFlatPixel(pos,rgb)
    
    def transpose(self):
        """
        Transposes the current image
        
        Transposing is tricky, as it is hard to remember which values have been changed 
        and which have not.  To simplify the process, we copy the current image and use
        that as a reference.  So we change the current image with setPixel, but read
        (with getPixel) from the copy.
        
        The transposed image will be drawn on the screen immediately afterwards.
        """
        current  = self.getCurrent()
        original = current.copy()
        current.setWidth(current.getHeight())
        
        for row in range(current.getHeight()):
            for col in range(current.getWidth()):
                current.setPixel(row,col,original.getPixel(col,row))
    
    def reflectHori(self):
        """
        Reflects the current image around the horizontal middle.
        """
        current = self.getCurrent()
        for h in range(current.getWidth()//2):
            for row in range(current.getHeight()):
                k = current.getWidth()-1-h
                current.swapPixels(row,h,row,k)
    
    def rotateRight(self):
        """
        Rotates the current image left by 90 degrees.
        
        Technically, we can implement this via a transpose followed by a vertical
        reflection. However, this is slow, so we use the faster strategy below.
        """
        current  = self.getCurrent()
        original = current.copy()
        current.setWidth(current.getHeight())
        
        for row in range(current.getHeight()):
            for col in range(current.getWidth()):
                current.setPixel(row,col,original.getPixel(original.getHeight()-col-1,row))
    
    def rotateLeft(self):
        """
        Rotates the current image left by 90 degrees.
        
        Technically, we can implement this via a transpose followed by a vertical
        reflection. However, this is slow, so we use the faster strategy below.
        """
        current  = self.getCurrent()
        original = current.copy()
        current.setWidth(current.getHeight())
        
        for row in range(current.getHeight()):
            for col in range(current.getWidth()):
                current.setPixel(row,col,original.getPixel(col,original.getWidth()-row-1))
    
    
    # ASSIGNMENT METHODS (IMPLEMENT THESE)
    def reflectVert(self):
        """ 
        Reflects the current image around the vertical middle.
        """
        #why does this work?
        current = self.getCurrent()
        for w in range(current.getHeight()//2):
            for col in range(current.getWidth()):
                k = current.getHeight()-1-w
                current.swapPixels(w, col, k, col)
    
    def monochromify(self, sepia):
        """
        Converts the current image to monochrome, using either greyscale or sepia tone.
        
        If `sepia` is False, then this function uses greyscale.  It removes all color 
        from the image by setting the three color components of each pixel to that pixel's 
        overall brightness, defined as 
            
            0.3 * red + 0.6 * green + 0.1 * blue.
        
        If sepia is True, it makes the same computations as before but sets green to
        0.6 * brightness and blue to 0.4 * brightness.
        
        Parameter sepia: Whether to use sepia tone instead of greyscale.
        Precondition: sepia is a bool
        """
        assert isinstance(sepia, bool)
        
        current = self.getCurrent()
        for pos in range(current.getLength()):
            rgb = current.getFlatPixel(pos)
            #rgb[0] = red
            brightness = 0.3 * rgb[0] + 0.6 * rgb[1] + 0.1 * rgb[2]
            if(sepia == False):
                newRGB = (int(brightness), int(brightness), int(brightness))
            else:
                newRGB = (rgb[0], int(0.6 * brightness), int(0.4 * brightness))
                #looks too dark??
            current.setFlatPixel(pos,newRGB)

    def jail(self):
        """
        Puts jail bars on the current image
        
        The jail should be built as follows:
        * Put 3-pixel-wide horizontal bars across top and bottom,
        * Put 4-pixel vertical bars down left and right, and
        * Put n 4-pixel vertical bars inside, where n is (number of columns - 8) // 50.
        
        The n+2 vertical bars should be as evenly spaced as possible.
        """
        current = self.getCurrent()
        self._drawHBar(0, (255, 0, 0))
        self._drawHBar(current.getHeight()-3, (255, 0, 0))
        self._drawVBar(0, (255, 0, 0))
        self._drawVBar(current.getWidth()-4, (255, 0, 0))
        
        #print('number of columns is ' + repr(current.getWidth()))
        n = (current.getWidth() - 8)//50
        #print('n = ' + repr(n))
        for x in range(n):
            #print(repr(current.getWidth()/(n+1)))
            col = int(round(current.getWidth()/(n+1))*(x+1))
            #print('col = ' + repr(col))
            self._drawVBar(col, (255, 0, 0))
        
        # n = (current.getWidth() - 8)//50    
        # for x in range(n+1):
        #     col = int(round(current.getWidth()//n*(x)))
        #     self._drawVBar(col, (255, 0, 0))
        
    
    def vignette(self):
        """
        Modifies the current image to simulates vignetting (corner darkening).
        
        Vignetting is a characteristic of antique lenses. This plus sepia tone helps
        give a photo an antique feel.
        
        To vignette, darken each pixel in the image by the factor
        
            1 - (d / hfD)^2
        
        where d is the distance from the pixel to the center of the image and hfD 
        (for half diagonal) is the distance from the center of the image to any of 
        the corners.
        """
        current = self.getCurrent()
        hfD = math.sqrt(current.getWidth()**2 + current.getHeight()**2)/2
        centerx = current.getWidth()/2
        centery = current.getHeight()/2
        for row in range(current.getHeight()):
            for col in range(current.getWidth()):
                factor = 1 - (math.sqrt((centerx-col)**2 + (centery-row)**2)/hfD)**2
                red = current.getPixel(row, col)[0] * factor
                green = current.getPixel(row, col)[1] * factor
                blue = current.getPixel(row, col)[2] * factor
                current.setPixel(row, col,
                        (int(round(red)), int(round(green)), int(round(blue))))
        
    
    def pixellate(self,step):
        """
        Pixellates the current image to give it a blocky feel.
        
        To pixellate an image, start with the top left corner (e.g. the first row and
        column).  Average the colors of the step x step block to the right and down
        from this corner (if there are less than step rows or step columns, go to the
        edge of the image). Then assign that average to ALL of the pixels in that block.
        
        When you are done, skip over step rows and step columns to go to the next 
        corner pixel.  Repeat this process again.  The result will be a pixellated image.
        
        Parameter step: The number of pixels in a pixellated block
        Precondition: step is an int > 0
        """
        assert isinstance(step, int) and step > 0
        
        current=self.getCurrent()
        # print('step is ' + repr(step) + ' height is ' + repr(current.getHeight()) +
        #       ' width is ' + repr(current.getWidth()))
        for x in range(0,current.getHeight(),step): # x = row
            if x+step<current.getHeight():
                step1=step
                # print('step1 is ' + repr(step1))
            else:
                step1=current.getHeight()-x
                # print('step1 is ' + repr(step1))
            for y in range(0,current.getWidth(),step):
                if y+step<current.getWidth():
                    step2=step
                    # print('step2 is ' + repr(step2))
                else:
                    step2=current.getWidth()-y
                    # print('step2 is ' + repr(step2))
                self._average(x,y,step1,step2)
               
                
                  
                    

    def encode(self, text):
        """
        Returns: True if it could hide the given text in the current image; False otherwise.
        
        This method attemps to hide the given message text in the current image.  It uses
        the ASCII representation of the text's characters.  If successful, it returns
        True.
        
        If the text has more than 999999 characters or the picture does not have enough
        pixels to store the text, this method returns False without storing the message.
        
        Parameter text: a message to hide
        Precondition: text is a string
        """
        assert isinstance(text, str)
        
        current = self.getCurrent()
        
        #start and end markers
        #start: 'START' + len(text) [using 0-6 pixels b/c 0-999999] ==> 5-11 pixels
        #standardize to 6 pixels for len
        lenText = str(len(text))
       # print('text len is ' + lenText)
        if len(lenText) < 6: #add 0s
            for x in range(6-len(lenText)):
                lenText = '0' + lenText
        #print('Start marker is ' + 'START' +lenText)
        
        newText = 'START' +  lenText + text
        
        lengthMSG = len(newText)
        numPixels = current.getLength()
        
        if(len(text) > 999999 or numPixels < lengthMSG):
            return False
        else:
            #actually encode
            for pos in range(len(newText)):
                newPixel = self._encode_pixel(pos, ord(newText[pos]))
                current.setFlatPixel(pos, newPixel)
            return True


    
    def decode(self):
        """
        Returns: The secret message stored in the current image.
        
        Detects message by determining if first 5 pixels decode to the
        start marker 'START'. The next 6 pixels decode to the length
        of the message.
        
        If no message is detected, it returns None
        """
        current = self.getCurrent()
        msg = ''
        start = ''
       
        #detect start
        for pos in range(11):
            start = start + chr(self._decode_pixel(pos))
        if(start[0:5] != 'START'):
            return None
        
        lenText = int(start[5:11])
       # print('start is ' + start + ' lenText is ' + repr(lenText))
        
        #while loop
        k = 11 #start after Start marker
        while k < lenText+11:   #take into account start marker
            char = chr(self._decode_pixel(k))
            msg = msg + char
            k = k+1
      
        return msg
    
    
    # HELPER FUNCTIONS
    def _drawHBar(self, row, pixel):
        """
        Draws a horizontal bar on the current image at the given row.
        
        This method draws a horizontal 3-pixel-wide bar at the given row of the current
        image. This means that the bar includes the pixels row, row+1, and row+2.
        The bar uses the color given by the pixel value.
        
        Parameter row: The start of the row to draw the bar
        Precondition: row is an int, with 0 <= row  &&  row+2 < image height
        
        Parameter pixel: The pixel color to use
        Precondition: pixel is a 3-element tuple (r,g,b) where each value is 0..255
        """
        assert isinstance(row, int) and 0<=row and row+2 < self.getCurrent().getHeight()
        assert isinstance(pixel, tuple) and len(pixel) == 3
        assert 0 <= pixel[0] and pixel[0] <= 255
        assert 0 <= pixel[1] and pixel[1] <= 255
        assert 0 <= pixel[2] and pixel[2] <= 255
        
        current = self.getCurrent()
        for col in range(current.getWidth()):
            current.setPixel(row,   col, pixel)
            current.setPixel(row+1, col, pixel)
            current.setPixel(row+2, col, pixel)
            
    def _drawVBar(self, col, pixel):
        """
        Draws a horizontal bar on the current image at the given row.
        
        This method draws a 4-pixel vertical bars at the given col of the current image.
        This means that the bar includes the pixels col, col+1, col+2, and col+3.
        The bar uses the color given by the pixel value.
        
        Parameter col: The start of the col to draw the bar
        Precondition: col is an int, with 0 <= col  &&  col+3 < image width
        
        Parameter pixel: The pixel color to use
        Precondition: pixel is a 3-element tuple (r,g,b) where each value is 0..255
        """
        #assert preconditions?
        assert isinstance(col, int) and 0<=col and col+3 < self.getCurrent().getWidth()
        assert isinstance(pixel, tuple) and len(pixel) == 3
        assert 0 <= pixel[0] and pixel[0] <= 255
        assert 0 <= pixel[1] and pixel[1] <= 255
        assert 0 <= pixel[2] and pixel[2] <= 255
        
        current = self.getCurrent()
        for row in range(current.getHeight()):
            current.setPixel(row, col, pixel)
            current.setPixel(row, col + 1, pixel)
            current.setPixel(row, col + 2, pixel)
            current.setPixel(row, col + 3, pixel)
    
    def _average(self, row, col, step1, step2):
        """
        Returns: the average of the rgb values in the pixel block
        
        This function averages the rgb values beginning at pixel(row,col) and going
        step pixels right and down
        
        Parameter row: The starting row of pixels to average
        Precondition: row is an int, with 0 <= row  &&  row + step1 <= image height
        
        Parameter col: The starting col of pixels to average
        Precondition: col is an int, with 0 <= col  &&  col + step2 <= image width
        
        Parameter step1: The positions down to average from starting row
        Precondition: step1 is an int >= 0
        
        Parameter step2: The positions right to average from starting col
        Precondition: step2 is an int >= 0        
        """
        assert isinstance(row, int) and 0<=row and isinstance(step1, int) and step1 >= 0
        assert isinstance(col, int) and 0<=col and isinstance(step2, int) and step2 >= 0 
        assert row+step1 <= self.getCurrent().getHeight() 
        assert col+step2 <= self.getCurrent().getWidth()

        current = self.getCurrent()
        sum_red=current.getPixel(row,col)[0]
        sum_green=current.getPixel(row,col)[1]
        sum_blue=current.getPixel(row,col)[2]
        for row1 in range(row,row+step1):
            for col1 in range(col,col+step2):
                sum_red=sum_red+current.getPixel(row1,col1)[0]
                sum_green=sum_green+current.getPixel(row1,col1)[1]
                sum_blue=sum_blue+current.getPixel(row1,col1)[2]
        for row1 in range(row,row+step1):
            for col1 in range(col,col+step2):
                avg = (int(round(sum_red/(step1*step2))),
                    int(round(sum_green/(step1*step2))),int(round(sum_blue/(step1*step2))))
                # if(row1 == row and col1 == col):
                #    print('average for row ' + repr(row1) + ' through ' + repr(row1+step1-1) +
                #    ' and col ' + repr(col1) +
                #          ' through ' + repr(col1+step2-1) + ' is ' + repr(avg))
                current.setPixel(row1,col1, avg)       
        
   
    def _decode_pixel(self, pos):
        """
        Returns: the number n that is hidden in pixel pos of the current image.
        
        This function assumes that the value was a 3-digit number encoded as the
        last digit in each color channel (e.g. red, green and blue).
        
        Parameter pos: a pixel position
        Precondition: pos is an int with  0 <= pos < image length (as a 1d list)
        """
        assert isinstance(pos, int) 
        assert 0 <= pos and pos < self.getCurrent().getLength()
        
        rgb = self.getCurrent().getFlatPixel(pos)
        red   = rgb[0]
        green = rgb[1]
        blue  = rgb[2]
        return  (red % 10) * 100  +  (green % 10) * 10  +  blue % 10
    
    def _encode_pixel(self, pos, msgASCII):
        """
        Returns: the pixel that hides a message in the current image.
        
        This function hides the ASCII code by changing the least significant
        digit of each color component to each digit of the ASCII code. Ex:
        If msgASCII = 107, (199, 222, 142) --> (191, 220, 147). If changing the last digit
        make the component > 255, then we change subtract 10 in addition to changing
        the least significant digit. Ex: msgASCII = 107, (199, 222, 255) -->
        (191, 220, 247).
        
        Parameter pos: a pixel position
        Precondition: pos is an int with  0 <= pos < image length (as a 1d list)
        
        Parameter msgASCII: an int that represents an ASCII code that needs to be encoded
        Precondition: msgASCII is an int between 0 and 255
        """
        assert isinstance(pos, int)
        assert 0 <= pos and pos < self.getCurrent().getLength()
        assert isinstance(msgASCII, int) and 0 <= msgASCII and msgASCII <= 255
        
        currentpixel = self.getCurrent().getFlatPixel(pos)
        red = currentpixel[0] - currentpixel[0]%10 + msgASCII//100
        green = currentpixel[1] - currentpixel[1]%10 + msgASCII%100//10
        blue = currentpixel[2] - currentpixel[2]%10 + msgASCII%10
        if (red > 255):
        	red=currentpixel[0] - currentpixel[0]%10 + msgASCII//100 - 10
        if (green > 255):
            green = currentpixel[1] - currentpixel[1]%10 + msgASCII%100//10 - 10
        if (blue > 255):
            blue = currentpixel[2] - currentpixel[2]%10 + msgASCII%10 - 10
        rgb = (int(red), int(green), int(blue))
        return rgb
        
        
        
    