from deparse import feature_order


class Segment:
    '''A representation of a phonetic segment, stored in terms of features.'''

    __slots__ = ['_positive', '_negative']

    def __init__(self, positive, negative):
        self._positive = positive
        self._negative = negative

    @classmethod
    def from_dictionary(cls, feature_dictionary):
        '''Initialise the segment from a dictionary of features. The feature name
        is the key, and the value is one of '+', '-', or '0'. The only ignored
        key is "IPA".'''

        positive = [key for key, value in feature_dictionary.items()
                    if value == '+']
        negative = [key for key, value in feature_dictionary.items()
                    if value == '-']

        return cls(positive, negative)

    @property
    def positive(self):
        return self._positive

    def add_positive(self, feature):
        '''Add the feature to the positive list. If it already exists in the
        negative list, remove it from negative.'''

        if feature not in self._positive:
            if feature in self._negative:
                self._negative.remove(feature)

            self._positive.append(feature)

    @property
    def negative(self):
        return self._negative

    def add_negative(self, feature):
        '''Add the feature to the negative list. If it already exists in the
        positive list, remove it from positive.'''

        if feature not in self._negative:
            if feature in self._positive:
                self._positive.remove(feature)

            self._negative.append(feature)

    def meets_conditions(self, conditions):
        '''Takes a dictionary of features, in the format:

            {'positive': ['feature1', 'feature2'], 'negative': ['feature3']}

        Returns True if all features specified as positive are in
        self._positive and those specified as negative are in self._negative.
        Otherwise returns false.

        '''

        # This code is really ugly. I had a cool one-liner using sets, but
        # switching to basic loops saved 8 seconds (!) when benchmarking.
        # Such is the life of optimisation.
        if 'positive' in conditions:
            for feature in conditions['positive']:
                if feature not in self._positive:
                    return False

        if 'negative' in conditions:
            for feature in conditions['negative']:
                if feature not in self._negative:
                    return False

        return True

    def __add__(self, other):
        '''Override the regular addition behaviour. When two segments are added
        together, the values of the second override those of the first that
        differ.'''
        new_segment = Segment(self._positive.copy(), self._negative.copy())

        for positive_feature in other.positive:
            new_segment.add_positive(positive_feature)

        for negative_feature in other.negative:
            new_segment.add_negative(negative_feature)

        return new_segment

    def __repr__(self):
        return '<Segment> Positive: {0}, Negative: {1}'.format(self._positive,
                                                               self._negative)


# A pseudo-segment that has all negative features, representing
# a word boundary
boundary = Segment(positive=[], negative=feature_order)
