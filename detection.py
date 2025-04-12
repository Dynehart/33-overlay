import os
from pprint import pprint
import cv2 as cv
import numpy as np
from collections import Counter

TemplatesFolder = "templates"
MapsFolder = "maps"
ResultsFolder = "results"


def detect_shape(file_path, template_path):
    img_rgb = cv.imread(file_path)
    assert img_rgb is not None, "file could not be read, check with os.path.exists()"
    template = cv.imread(template_path, cv.IMREAD_GRAYSCALE)
    assert (
        template is not None
    ), "template could not be read, check with os.path.exists()"

    data = []

    # lower threshold is less strict
    # chests require a higher value to distinguish elite and regular
    # 0.8 and 2 have worked well there
    # urns may require ~0.75 and ~3.5
    threshold = 0.78
    tolerance = 5  # fairly large numbers should be safe

    if template_path.rfind("urn") != -1:
        threshold = 0.7

    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
    w, h = template.shape[::-1]
    res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)

    for pt in zip(*loc[::-1]):
        x = pt[0] + w / 2
        y = pt[1] + h / 2

        data.append([x.item(), y.item()])
        cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

    result = group_similar_values(data, tolerance)

    file_name = os.path.basename(file_path)
    template_name = os.path.basename(template_path)
    output_file = os.path.splitext(file_name)[0] + "_" + template_name

    print("found", len(result), "of", output_file)
    pprint(result)

    output = os.path.join(ResultsFolder, output_file)

    # save file in debug mode with concatinated file+template
    if __debug__ and len(result) > 0:
        cv.imwrite(output.lower(), img_rgb)


def get_mode(numbers):
    counter = Counter(numbers)
    return counter.most_common(1)[0][0]


def group_similar_values(numbers, tolerance=1.0):
    groups = []

    for x, y in numbers:
        # Try to find an existing group to add this pair to
        added_to_group = False
        for group in groups:
            if not group[0]:
                group.append([x, y])
                added_to_group = True
                break

            mode_x, mode_y = group[0]
            # If the x and y values are within the tolerance of any group, add to it
            if abs(x - mode_x) <= tolerance and abs(y - mode_y) <= tolerance:
                group.append([x, y])
                added_to_group = True
                break

        # If this pair wasn't added to any group, create a new group
        if not added_to_group:
            groups.append([[x, y]])

    # Now, calculate the mode for x and y in each group
    result = []
    for group in groups:
        x_values = [x for x, y in group]
        y_values = [y for x, y in group]
        mode_x = get_mode(x_values)
        mode_y = get_mode(y_values)
        result.append([mode_x, mode_y])

    return result


for file_name in os.listdir(MapsFolder):
    for template_name in os.listdir(TemplatesFolder):
        file_path = os.path.join(MapsFolder, file_name)
        template_path = os.path.join(TemplatesFolder, template_name)

        if os.path.isdir(file_path) or os.path.isdir(template_path):
            continue

        detect_shape(file_path, template_path)

# detect_shape('purple.png', 'urn.png')
