import SwiftUI
import WatchKit

struct ContentView: View {
    @State private var showAlert = false

    var body: some View {
        VStack {
            Spacer()

            //Logo
            Image("WAvE")
                .resizable()
                .scaledToFit()
                .frame(width: 50, height: 50)
                .clipShape(Circle())
                .overlay(Circle().stroke(Color.blue, lineWidth: 2))

            Text("Looks like you're")
                .font(.headline)
                .foregroundColor(Color.blue)

            Text("fatigued!")
                .font(.headline)
                .foregroundColor(Color.blue)

            Spacer()
            Spacer()

            // Dismiss button
            Button(action: {
                self.showAlert = true
                WKInterfaceDevice.current().play(.notification)
            }) {
                Text("Dismiss")
                    .foregroundColor(Color.white)
                    .padding()
                    .background(Capsule().fill(Color.blue))
            }
            
            Spacer()
        }
        .onAppear {
            // Play Haptic
            WKInterfaceDevice.current().play(.notification)
        }
        
        .alert(isPresented: $showAlert) {
            Alert(title: Text("Please refer to your EFB for further instructions"),
                  dismissButton: .default(Text("OK")))
        }
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
func playHaptic() {
    WKInterfaceDevice.current().play(.notification)
    }
