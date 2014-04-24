# -*- coding:utf-8 -*- 


#
# Inspired from :
#
#       - Nate Robins' Programs
#         http://www.xmission.com/~nate
#
#       - NeHe Productions - ArcBall Rotation Tutorial
#         http://nehe.gamedev.net
#


#
# External dependencies
#
from math import cos, sin, pi, sqrt
from numpy import array, identity, zeros, float32, dot, cross


#
# Create a trackball for smooth object transformation
#
class Trackball :


	#
	# Initialisation
	#
	def __init__( self, width, height ) :

		# Window size
		self.width = width
		self.height = height

		# Button pressed
		self.button = 0

		# Mouse position
		self.previous_mouse_position = [ 0, 0 ]

		# Tranformation matrix
		self.transformation = identity( 4, dtype=float32 )


	#
	# Reset the current transformation
	#
	def Reset( self ) :

		# Reset the tranformation matrix
		self.transformation = identity( 4, dtype=float32 )


	#
	# Resize the viewing parameters
	#
	def Resize( self, width, height ) :

		# Change window size
		self.width = width
		self.height = height


	#
	# Handle when a mouse button is pressed
	#
	def MousePress( self, mouse_position, button ) :

		# Record mouse position
		self.previous_mouse_position = mouse_position

		# Record button pressed
		self.button = button


	#
	# Handle when a mouse button is released
	#
	def MouseRelease( self ) :

		# Mouse button release
		self.button = 0


	#
	# Handle when the mouse wheel is used
	#
	def WheelEvent( self, delta ) :

		# Compute the Z-translation
		translation = zeros( 3 )
		translation[2] -= delta * 2.0

		# Project the translation vector to the object space
		translation = dot( self.transformation[:3,:3], translation )

		# Translate the transformation matrix
		m = self.transformation
		m[3] = m[0] * translation[0] + m[1] * translation[1] + m[2] * translation[2] + m[3]


	#
	# Handle when the mouse is moved
	#
	def Motion( self, current_mouse_position ) :

		# Rotation
		if self.button == 1 :

			# Map the mouse positions
			previous_position = self.TrackballMapping( self.previous_mouse_position )
			current_position = self.TrackballMapping( current_mouse_position )

			# Project the rotation axis to the object space
			rotation_axis = dot( self.transformation[:3,:3], cross( previous_position, current_position ) )

			# Rotation angle
			rotation_angle = sqrt( ((current_position - previous_position)**2).sum() ) * 2.0

			# Create a rotation matrix according to the given angle and axis
			c, s = cos( rotation_angle ), sin( rotation_angle )
			n = sqrt( (rotation_axis**2).sum() )
			if n == 0 : n = 1.0
			rotation_axis /= n
			x, y, z = rotation_axis
			cx, cy, cz = (1 - c) * x, (1 - c) * y, (1 - c) * z
			R = array([ [   cx*x + c, cy*x - z*s, cz*x + y*s, 0],
					[ cx*y + z*s,   cy*y + c, cz*y - x*s, 0],
					[ cx*z - y*s, cy*z + x*s,   cz*z + c, 0],
					[          0,          0,          0, 1] ], dtype=float32 ).T

			# Rotate the transformation matrix
			self.transformation = dot( R, self.transformation )

		# XY translation
		elif self.button ==  2 :

			# Compute the XY-translation
			translation = zeros( 3 )
			translation[0] -= (self.previous_mouse_position[0] - current_mouse_position[0])*0.02
			translation[1] += (self.previous_mouse_position[1] - current_mouse_position[1])*0.02

			# Project the translation vector to the object space
			translation = dot( self.transformation[:3,:3], translation )

			# Translate the transformation matrix
			m = self.transformation
			m[3] = m[0] * translation[0] + m[1] * translation[1] + m[2] * translation[2] + m[3]

		# No update
		else : return False

		# Save the mouse position
		self.previous_mouse_position = current_mouse_position

		# Require a display update
		return True

	
	#
	# Map the mouse position onto a unit sphere
	#
	def TrackballMapping( self, mouse_position ) :

		v = zeros( 3 )
		v[0] = ( 2.0 * mouse_position[0] - self.width ) / self.width
		v[1] = ( self.height - 2.0 * mouse_position[1] ) / self.height
		d = sqrt(( v**2 ).sum())
		if d > 1.0 : d = 1.0
		v[2] = cos( pi / 2.0 * d )
		return v / sqrt(( v**2 ).sum())