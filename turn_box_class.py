import bpy
import math

class Box():
    def __init__(self, name, pos, tate):
        self.name = name
        self.tate = True
        
        bpy.ops.mesh.primitive_cube_add(size=1)
        obj = bpy.context.object
        obj.name = name
        obj.scale = (1, 2, 0.1)
        
        # 原点を左上にする
        cursor = bpy.context.scene.cursor				# 3Dカーソル
        cx, cy, cz = cursor.location		  # 現在の3Dカーソルの位置
        
        x, y, z = obj.location                      # オブジェクトの位置（初期状態ではオブジェクトの中心が原点）
        x -= obj.dimensions[0] / 2                  # x方向の原点をずらす
        y += obj.dimensions[1] / 2                  # y方向の原点をずらす
        z -= obj.dimensions[2] / 2                  # z方向の原点をずらす
        cursor.location = (x, y, z)                 # 修正後のカーソル位置
        bpy.ops.object.origin_set(type="ORIGIN_CURSOR", center="MEDIAN")
        cursor.location = (cx, cy, cz)		# 3Dカーソルを当初の位置に戻す
        self.put(pos)
        
    def put(self, pos):
        obj = bpy.data.objects[self.name]
        self.pos = pos
        obj.location = pos
    
    def normalturn(self):
        obj = bpy.data.objects[self.name]
        obj.rotation_euler = (0, 0, math.radians(90))
    
    def lefttopturn(self):
        # 原点に設定したい頂点に3Dカーソルを設定する
        obj = bpy.data.objects[self.name]
        obj.rotation_euler = (0, 0, math.radians(90))
        x, y, z = self.pos
        cursor = bpy.context.scene.cursor				# 3Dカーソル
        cx, cy, cz = cursor.location		# 現在の3Dカーソルの位置
        # bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY", center="BOUNDS")
        cursor.location = (x, y, z)
        self.put((x, y-obj.dimensions[0], z))
        print(x,y,z)
        bpy.ops.object.origin_set(type="ORIGIN_CURSOR", center="MEDIAN")
        cursor.location = (cx, cy, cz)		# 3Dカーソルを当初の位置に戻す

def main():
    box1 = Box("A", (0, 0, 0), True)
    box2 = Box("B", (3, 0, 0), True)
    box3 = Box("C", (6, 0, 0), True)
    
    box2.normalturn()
    box3.lefttopturn()


if __name__ == "__main__":
    main()
