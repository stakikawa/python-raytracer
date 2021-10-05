from Original.color import Color
from Original.color import write_color
from Original.hittable import HitRecord
from Original.hittable_list import HittableList
from Original.point3 import Point3
from Original.sphere import Sphere
from Original.vec3 import Vec3
from Original.vec3 import unit_vector
from Original.vec3 import random_vec
from Original.vec3 import random_vec_mm
from Original.lambertian import Lambertian
from Original.dielectric import Dielectric
from Original.metal import Metal
from Original.camera import Camera
from Original.utility import INFINITY
from Original.utility import random_double
import math


def random_scene():
    world = HittableList()

    ground_material = Lambertian(Color(0.5, 0.5, 0.5))
    world.add(Sphere(Point3(0, -1000, 0), 1000, ground_material))

    for a in range(-11, 11):
        for b in range(-11, 11):
            choose_mat = random_double()
            center = Point3(a + 0.9 * random_double(), 0.2, b + 0.9 * random_double())

            if (center - Point3(4, 0.2, 0)).length() > 0.9:

                if choose_mat < 0.8:
                    # diffuse
                    albedo = random_vec() * random_vec()
                    sphere_material = Lambertian(albedo)
                    world.add(Sphere(center, 0.2, sphere_material))
                elif choose_mat < 0.95:
                    # metal
                    albedo = random_vec_mm(0.5, 1)
                    fuzz = random_double(0, 0.5)
                    sphere_material = Metal(albedo, fuzz)
                    world.add(Sphere(center, 0.2, sphere_material))
                else:
                    # glass
                    sphere_material = Dielectric(1.5)
                    world.add(Sphere(center, 0.2, sphere_material))

    material1 = Dielectric(1.5)
    world.add(Sphere(Point3(0, 1, 0), 1.0, material1))

    material2 = Lambertian(Color(0.4, 0.2, 0.1))
    world.add(Sphere(Point3(-4, 1, 0), 1.0, material2))

    material3 = Metal(Color(0.7, 0.6, 0.5))
    world.add(Sphere(Point3(4, 1, 0), 1.0, material3))

    return world


def ray_color(r, world, depth):
    rec = HitRecord()
    if depth <= 0:
        return Color(0, 0, 0)
    if world.hit(r, 0.001, INFINITY, rec):
        valid, attenuation, scattered = rec.material.scatter(r, rec)
        if valid:
            return attenuation * ray_color(scattered, world, depth - 1)
        return Color(0, 0, 0)
    unit_direction = unit_vector(r.direction)
    t = 0.5 * (unit_direction.y() + 1.0)
    return (1.0 - t) * Color(1.0, 1.0, 1.0) + t * Color(0.5, 0.7, 1.0)


def main():
    # Image
    aspect_ratio = 3.0 / 2.0
    image_width = 1200
    image_height = math.floor(image_width / aspect_ratio)
    samples_per_pixel = 500
    max_depth = 50

    # World
    world = random_scene()

    # Camera
    lookfrom = Point3(13, 2, 3)
    lookat = Point3(0, 0, 0)
    vup = Vec3(0, 1, 0)
    dist_to_focus = 10.0
    aperture = 0.1
    fov = 20.0

    cam = Camera(lookfrom, lookat, vup, fov, aspect_ratio, aperture, dist_to_focus)

    # Render
    anti_alias = True
    print("P3\n", image_width, ' ', image_height, "\n255\n")

    for j in range(image_height - 1, -1, -1):
        for i in range(image_width):
            pixel_color = Color(0, 0, 0)
            if anti_alias:
                for s in range(samples_per_pixel):
                    u = float(i + random_double()) / (image_width - 1)
                    v = float(j + random_double()) / (image_height - 1)
                    r = cam.get_ray(u, v)
                    pixel_color += ray_color(r, world, max_depth)
                write_color(pixel_color, samples_per_pixel)
            else:
                u = float(i) / (image_width - 1)
                v = float(j) / (image_height - 1)
                r = cam.get_ray(u, v)
                pixel_color += ray_color(r, world, max_depth)
                write_color(pixel_color)


main()