
# Convert "bind camera to marker" to sequencer scene-strips
# by tintwotin 

bl_info = {
	"name": "Camera Markers to Scene Strips",
	"description": "Converts Camera Bind-To-Markers to Scene Strips",
	"author": "tintwotin",
	"version": (1, 1),
	"blender": (2, 7, 9),
	"location": "VSE strip editor > Header > Add Menu: Marker Cameras",
	"wiki_url": "https://github.com/tin2tin/Camera-Markers-to-Scene-Strips/wiki",
	"tracker_url":"",
	"category": "Sequencer"}

import bpy

class SEQUENCE_OT_convert_cameras(bpy.types.Operator):
	"""Converts Camera Bind-To-Markers to Scene Strips"""
	bl_label = "Marker Cams"
	bl_idname = "sequencer.convert_cameras"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		scene=bpy.context.scene

		if not bpy.context.scene.sequence_editor: #create sequence, if missing
			bpy.context.scene.sequence_editor_create()   

		marker_camera=[]
		marker_frame=[]

		for marker in scene.timeline_markers: #find the cameras and their frame

			if marker.camera:   			
				marker_camera.append(marker.camera.name)
				marker_frame.append(marker.frame)

		if len(marker_camera)==0:         # cancel if no cameras
			return {'CANCELLED'}

		cnt=0

		for i in marker_camera:           #add cameras to sequencer   		 
			cf = marker_frame[cnt]
			addSceneIn = cf

			if cnt<len(marker_camera)-1: # add out frame
				addSceneOut = marker_frame[cnt+1]
			else:    
				addSceneOut = bpy.context.scene.frame_end+1 #last clip extented to end of range

			addSceneChannel = 1          # attempt to add in this channel - if full strips will be moved upwards
			addSceneTlStart = cf		

            # add scene strip in current scene at in and out frame numbers
			newScene=bpy.context.scene.sequence_editor.sequences.new_scene('Scene', bpy.context.scene, addSceneChannel, addSceneTlStart)
			newScene=bpy.context.scene.sequence_editor.sequences_all[newScene.name]
			newScene.scene_camera = bpy.data.objects[marker_camera[cnt]]
			newScene.animation_offset_start = addSceneIn
			newScene.frame_final_end = addSceneOut
			newScene.frame_start = cf  
			cnt+=1

		return {'FINISHED'}

def panel_append(self, context):
	self.layout.operator(SEQUENCE_OT_convert_cameras.bl_idname)

def register():
	bpy.utils.register_class(SEQUENCE_OT_convert_cameras)
	bpy.types.SEQUENCER_MT_add.append(panel_append) # add to "add" vse header menu

def unregister():
	bpy.utils.unregister_class(SEQUENCE_OT_convert_cameras)
	bpy.types.SEQUENCER_MT_add.remove(panel_append)

if __name__ == "__main__":
	register() 

#unregister()     
