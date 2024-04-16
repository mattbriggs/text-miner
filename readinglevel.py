''' Reading Level
    Calculates the Flesch Index for the reading level of the text.

    Input: Ingests a file and scores the reading level.
    Output: The reading level.

'''

def get_reading_level(textstring):
    '''Calculates the Flesch Index for the reading level of the text.'''
    try:
        sentence=textstring.count(".") + textstring.count('!') + textstring.count(";") + textstring.count(":") + textstring.count("?")

        words=len(textstring.split())
        syllable=0

        for word in textstring.split():
            for vowel in ['a','e','i','o','u']:
                syllable += word.count(vowel)
            for ending in ['es','ed','e']:
                if word.endswith(ending):
                    syllable -= 1
            if word.endswith('le'):
                    syllable += 1

        level = round((0.39*words)/sentence+ (11.8*syllable)/words-15.59)
        message = {"level" : level}
    except Exception as e:
        message = {"level" : e}

    return message

def main():
    print("This is the script that contains the functional logic.")

if __name__ == "__main__":
    main()